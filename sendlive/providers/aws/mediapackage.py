from pydantic import BaseModel


class MediaPackageV2Channel(BaseModel):
    """Represents a MediaPackageV2 channel."""

    name: str
    arn: str


class MediaPackageV2ChannelGroup(BaseModel):
    """Represents a MediaPackageV2 channel group."""

    name: str
    """The ID of the channel group."""
    arn: str
    """The ARN of the channel group."""

    channels: list[MediaPackageV2Channel] = []
