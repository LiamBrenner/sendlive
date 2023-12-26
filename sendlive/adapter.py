from abc import ABC, abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from sendlive.constants import BaseCredential, ProviderOptions
from sendlive.stream import BaseStream


class BaseAdapter(BaseModel, ABC):
    """Base class for all cloud provider adapters."""

    credentials: BaseCredential
    provider_options: Optional[ProviderOptions] = None

    # @abstractmethod
    # def setup_provider(self) -> None:
    #     """Run any required steps to setup the cloud provider, such as creating a client and setting it on the adapter instance."""

    @abstractmethod
    def setup_stream(self) -> None:
        """Run setup and preparation required before the stream can be started.

        This method creates and configures any required resources for the stream, but does not actually begin the live stream.
        """

    @abstractmethod
    def list_streams(self) -> list[str]:
        """Fetch a list of all streams from the cloud provider."""

    @abstractmethod
    def create_stream(self, name: str) -> BaseStream:
        """Create a new stream on the cloud provider."""

    def __init__(self, credentials: BaseCredential, *args: Any, **kwargs: Any) -> None:
        """Init the adapter and perform any required cloud provider setup steps."""
        super().__init__(*args, credentials=credentials, **kwargs)
        # self.setup_provider()
