from typing import Any

from pydantic import BaseModel

from sendlive.adapter import BaseAdapter
from sendlive.constants import (
    BaseCredential,
    ServiceProvider,
)


class SendLiveConfig(BaseModel):
    """Configuration for the different cloud vendors and their respective credentials."""

    credentials: BaseCredential

    adapter: BaseAdapter

    def __init__(self, credentials: BaseCredential, **data: Any) -> None:
        """Init the config and create the adapter based on the provided credentials."""
        super().__init__(credentials=credentials, **data)
        self.adapter = credentials.adapter_cls(credentials=self.credentials)

    @property
    def service_provider(self) -> ServiceProvider:
        """Return the service provider, based on the provided credentials."""
        return self.credentials.service_provider
