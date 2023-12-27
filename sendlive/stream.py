from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseStream(BaseModel, ABC):
    """BaseStream is an abstract class that defines the interface for all individual stream implementations.

    This class is meant to only represent one individual stream.
    """

    name: str

    @abstractmethod
    def start(self) -> None:
        """Start the stream."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the stream."""

    @abstractmethod
    def is_alive(self) -> None:
        """Check if the stream is alive."""

    @abstractmethod
    def get_url(self) -> None:
        """Get the URL for the stream."""

    @abstractmethod
    def get_name(self) -> None:
        """Get the name of the stream."""
