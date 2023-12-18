"""Main sendlive package."""
from pydantic import BaseModel

from sendlive.config import SendLiveConfig
from sendlive.constants import ServiceProvider


class SendLive(BaseModel):
    """SendLive is a library for creating live streams with different cloud vendors, using one interface."""

    config: SendLiveConfig

    @property
    def service_provider(self) -> ServiceProvider:
        """Return the service provider, based on the provided credentials."""
        return self.config.service_provider
