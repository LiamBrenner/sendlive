"""Specific implementations and adaptations for the different supported cloud providers."""
from abc import ABC

from pydantic import BaseModel


class BaseProvider(BaseModel, ABC):
    """Base class for all cloud providers."""
