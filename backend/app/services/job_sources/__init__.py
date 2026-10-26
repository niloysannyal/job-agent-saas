from typing import List, Optional, Sequence

from app.core.config import settings
from app.services.job_sources.base import JobSource
from app.services.job_sources.adzuna import AdzunaJobSource
from app.services.job_sources.remotive import RemotiveJobSource
from app.services.job_sources.remoteok import RemoteOKJobSource
from app.services.job_sources.greenhouse import GreenhouseJobSource
from app.services.job_sources.lever import LeverJobSource
from app.services.job_sources.freehire import FreehireJobSource
from app.services.job_sources.exceptions import (
    JobSourceConfigError,
    JobSourceError,
    JobSourceHTTPError,
)


def get_available_sources(source_names: Optional[Sequence[str]] = None) -> List[JobSource]:
    """
    Return instantiated JobSource instances based on requested names or all defaults.
    Supported keys: 'adzuna', 'remotive', 'remoteok', 'greenhouse', 'lever', 'freehire'.
    """
    available_map = {
        "adzuna": lambda: AdzunaJobSource(),
        "remotive": lambda: RemotiveJobSource(),
        "remoteok": lambda: RemoteOKJobSource(),
        "greenhouse": lambda: GreenhouseJobSource(),
        "lever": lambda: LeverJobSource(),
        "freehire": lambda: FreehireJobSource(),
    }
    if source_names is not None:
        selected_sources: List[JobSource] = []
        for name in source_names:
            key = name.strip().lower()
            if key in available_map:
                selected_sources.append(available_map[key]())
        return selected_sources

    # Default to zero-config sources
    sources: List[JobSource] = [
        RemotiveJobSource(),
        RemoteOKJobSource(),
        GreenhouseJobSource(),
        LeverJobSource(),
        FreehireJobSource(),
    ]
    # Include Adzuna if credentials configured
    if settings.ADZUNA_APP_ID and settings.ADZUNA_APP_KEY:
        sources.append(AdzunaJobSource())

    return sources


__all__ = [
    "JobSource",
    "AdzunaJobSource",
    "RemotiveJobSource",
    "RemoteOKJobSource",
    "GreenhouseJobSource",
    "LeverJobSource",
    "FreehireJobSource",
    "JobSourceError",
    "JobSourceConfigError",
    "JobSourceHTTPError",
    "get_available_sources",
]
