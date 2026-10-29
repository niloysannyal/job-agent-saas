import logging
from urllib.parse import urlparse
from arq import cron
from arq.connections import RedisSettings

from app.core.config import settings
from app.workers.tasks import (
    ingest_jobs_task,
    embed_jobs_batch_task,
    monitor_followups_task,
    reflect_experience_task,
)

logger = logging.getLogger(__name__)


def parse_redis_settings(url: str) -> RedisSettings:
    """Parse a redis connection URL into an arq RedisSettings instance."""
    parsed = urlparse(url)
    return RedisSettings(
        host=parsed.hostname or "localhost",
        port=parsed.port or 6379,
        password=parsed.password,
        database=int(parsed.path.lstrip("/") or 0) if parsed.path else 0,
    )


async def startup(ctx):
    logger.info("Initializing Arq Job Agent background worker...")


async def shutdown(ctx):
    logger.info("Shutting down Arq Job Agent background worker...")


class WorkerSettings:
    """Arq Worker settings configuration."""
    functions = [
        ingest_jobs_task,
        embed_jobs_batch_task,
        monitor_followups_task,
        reflect_experience_task,
    ]
    cron_jobs = [
        cron(monitor_followups_task, hour={9, 18}, minute=0),
    ]
    redis_settings = parse_redis_settings(settings.REDIS_URL)
    on_startup = startup
    on_shutdown = shutdown
    max_jobs = 10
    job_timeout = 300
