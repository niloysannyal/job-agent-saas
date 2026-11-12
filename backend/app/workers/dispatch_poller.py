"""
backend/app/workers/dispatch_poller.py

PostgreSQL DB Outbox Poller Worker Daemon for Outbound Dispatch.
Polls hold_queue_items using SELECT ... FOR UPDATE SKIP LOCKED.
Includes a continuous 30-second periodic sweeper for stale claimed and sending items.

Usage:
  python -m app.workers.dispatch_poller [--poll-interval 5] [--batch-size 10]
"""

import asyncio
from datetime import datetime, timedelta, timezone
import logging
import signal
import sys
from typing import Dict, List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.session import normalize_db_url
from app.models.dispatch import HoldQueueItem
from app.services.dispatch.gateway import SendGateway

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [poller] %(message)s")
logger = logging.getLogger("dispatch_poller")


def sweep_stale_items(db: Session) -> Dict[str, int]:
    """
    Periodic 30-second sweeper per Section 3.2 of specification:
    1. Stale claimed items (>30s) are reset back to 'pending'.
    2. Stale sending items (>60s) transition to 'unknown' (preserving reservation).
    """
    now = datetime.now(timezone.utc)
    claim_timeout = now - timedelta(seconds=30)
    sending_timeout = now - timedelta(seconds=60)

    # 1. Reset stale claimed -> pending
    swept_claimed = (
        db.query(HoldQueueItem)
        .filter(
            HoldQueueItem.status == "claimed",
            HoldQueueItem.claimed_at < claim_timeout,
        )
        .update(
            {"status": "pending", "claimed_at": None},
            synchronize_session=False,
        )
    )

    # 2. Transition stale sending -> unknown
    swept_sending = (
        db.query(HoldQueueItem)
        .filter(
            HoldQueueItem.status == "sending",
            HoldQueueItem.sending_started_at < sending_timeout,
        )
        .update(
            {"status": "unknown"},
            synchronize_session=False,
        )
    )

    if swept_claimed > 0 or swept_sending > 0:
        db.commit()
        logger.info(
            "Sweeper completed: reset %d stale claimed to pending; transitioned %d stale sending to unknown",
            swept_claimed, swept_sending,
        )

    return {"swept_claimed": swept_claimed, "swept_sending": swept_sending}


def claim_pending_batch(db: Session, batch_size: int = 10) -> List[str]:
    """
    Claim a batch of eligible hold items using SELECT ... FOR UPDATE SKIP LOCKED.
    Returns list of claimed hold item IDs.
    """
    now = datetime.now(timezone.utc)

    # Query items ready to be dispatched
    query = (
        db.query(HoldQueueItem)
        .filter(
            HoldQueueItem.status == "pending",
            HoldQueueItem.release_at <= now,
        )
        .order_by(HoldQueueItem.release_at.asc())
        .limit(batch_size)
        .with_for_update(skip_locked=True)
    )

    eligible_items = query.all()
    if not eligible_items:
        return []

    claimed_ids = []
    for item in eligible_items:
        item.status = "claimed"
        item.claimed_at = now
        claimed_ids.append(item.id)

    db.commit()
    logger.info("Atomically claimed batch of %d hold items with SKIP LOCKED", len(claimed_ids))
    return claimed_ids


async def poll_and_dispatch_batch(db: Session, batch_size: int = 10) -> int:
    """
    Poll, claim, and execute dispatch for one batch of hold items.
    Returns count of items processed.
    """
    if settings.DISPATCH_GLOBAL_KILL_SWITCH:
        logger.warning("DISPATCH_GLOBAL_KILL_SWITCH is ACTIVE. Skipping dispatch poll.")
        return 0

    claimed_ids = claim_pending_batch(db, batch_size=batch_size)
    if not claimed_ids:
        return 0

    dispatched_count = 0
    for item_id in claimed_ids:
        try:
            success = await SendGateway.dispatch_hold_item(db, item_id)
            if success:
                dispatched_count += 1
        except Exception as e:
            logger.error("Unexpected error dispatching hold item %s: %s", item_id, e, exc_info=True)

    return dispatched_count


async def run_poller_daemon(
    db_url: Optional[str] = None,
    poll_interval: float = 5.0,
    batch_size: int = 10,
    stop_event: Optional[asyncio.Event] = None,
) -> None:
    """
    Continuous poller daemon loop.
    Runs every `poll_interval` seconds until `stop_event` is set.
    """
    url = normalize_db_url(db_url or settings.DATABASE_URL)
    engine = create_engine(url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    logger.info("Dispatch Poller Daemon started (poll_interval=%.1fs, batch_size=%d)", poll_interval, batch_size)
    last_sweep = datetime.now(timezone.utc) - timedelta(seconds=35)

    if stop_event is None:
        stop_event = asyncio.Event()

    try:
        while not stop_event.is_set():
            now = datetime.now(timezone.utc)
            with SessionLocal() as db:
                # 1. Run 30s sweeper if due
                if (now - last_sweep).total_seconds() >= 30.0:
                    try:
                        sweep_stale_items(db)
                    except Exception as e:
                        logger.error("Error during stale item sweep: %s", e)
                    last_sweep = now

                # 2. Poll and dispatch pending batch
                try:
                    await poll_and_dispatch_batch(db, batch_size=batch_size)
                except Exception as e:
                    logger.error("Error during dispatch batch: %s", e)

            # Sleep until next poll or shutdown
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=poll_interval)
            except asyncio.TimeoutError:
                pass

    finally:
        logger.info("Dispatch Poller Daemon stopping...")
        engine.dispose()
        logger.info("Dispatch Poller Daemon terminated cleanly.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="JobEazy Outbound Dispatch Poller Daemon")
    parser.add_argument("--poll-interval", type=float, default=5.0, help="Seconds between polls")
    parser.add_argument("--batch-size", type=int, default=10, help="Max items per claim batch")
    parser.add_argument("--db-url", type=str, default=None, help="Database URL")
    args = parser.parse_args()

    stop_event = asyncio.Event()

    def handle_signal(sig, frame):
        logger.info("Received signal %s. Initiating graceful shutdown...", sig)
        stop_event.set()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    asyncio.run(
        run_poller_daemon(
            db_url=args.db_url,
            poll_interval=args.poll_interval,
            batch_size=args.batch_size,
            stop_event=stop_event,
        )
    )


if __name__ == "__main__":
    main()

