from pydantic import BaseModel


class MediaPackageV2ChannelOriginEndpoint(BaseModel):
    """Represents a MediaPackageV2 channel origin endpoint."""

    name: str
    """The ID of the origin endpoint."""
    arn: str
    """The ARN of the origin endpoint."""
    url: str
    """The URL of the origin endpoint."""


class MediaPackageV2Channel(BaseModel):
    """Represents a MediaPackageV2 channel."""

    name: str
    arn: str

    origin_endpoints: list[MediaPackageV2ChannelOriginEndpoint] = []


class MediaPackageV2ChannelGroup(BaseModel):
    """Represents a MediaPackageV2 channel group."""

    name: str
    """The ID of the channel group."""
    arn: str
    """The ARN of the channel group."""

    channels: list[MediaPackageV2Channel] = []
