from collections.abc import Mapping
from http import HTTPStatus
from typing import Any, Optional

from boto3.session import Session
from mypy_boto3_medialive import MediaLiveClient
from mypy_boto3_medialive.type_defs import (
    CreateInputSecurityGroupResponseTypeDef,
    InputSecurityGroupTypeDef,
)
from mypy_boto3_mediapackagev2 import mediapackagev2Client
from mypy_boto3_mediapackagev2.literals import ContainerTypeType
from mypy_boto3_mediapackagev2.type_defs import (
    CreateChannelGroupRequestRequestTypeDef,
    CreateChannelGroupResponseTypeDef,
    CreateChannelResponseTypeDef,
    CreateOriginEndpointResponseTypeDef,
)
from pydantic import BaseModel, PrivateAttr, computed_field

from sendlive.constants import AWSCredentials, AWSOptions
from sendlive.exceptions import SendLiveError
from sendlive.logger import logger
from sendlive.mixins import TagMixin
from sendlive.providers.aws.mediapackage import (
    MediaPackageV2Channel,
    MediaPackageV2ChannelGroup,
)


class AWSBaseMixin(BaseModel, TagMixin):
    """Base mixin for AWS operations."""

    _boto_session: Session = PrivateAttr()
    provider_options: Optional[AWSOptions] = None

    def __init__(self, credentials: AWSCredentials, **data: dict[Any, Any]) -> None:
        """Set up boto session."""
        super().__init__(credentials=credentials, **data)
        self._boto_session = Session(
            aws_access_key_id=credentials.access_key,
            aws_secret_access_key=credentials.secret_key.get_secret_value(),
            region_name=credentials.region,
        )


class MediaLiveMixin(AWSBaseMixin):
    """Mixin for MediaLive operations."""

    @computed_field  # type: ignore[misc]
    @property
    def medialive(self) -> MediaLiveClient:
        """Return medialive boto3 client."""
        return self._boto_session.client("medialive")

    def create_input_security_group(self) -> InputSecurityGroupTypeDef:
        """Create a medialive input security group and return it."""
        if not self._boto_session:
            raise SendLiveError("Boto session not set up.")
        input_security_group: CreateInputSecurityGroupResponseTypeDef = (
            self.medialive.create_input_security_group(
                WhitelistRules=[{"Cidr": "0.0.0.0/0"}],
                Tags=self.get_operation_tags(),
            )
        )
        if (
            input_security_group["ResponseMetadata"]["HTTPStatusCode"]
            != HTTPStatus.CREATED
        ):
            raise SendLiveError(
                f"Failed to create input security group, received non 201 created response: {input_security_group}"
            )
        new_input_security_group: InputSecurityGroupTypeDef = input_security_group[
            "SecurityGroup"
        ]
        if "Id" not in new_input_security_group:
            raise SendLiveError("Created input security group did not return an id.")
        logger.info(f"\n\nINPUT SEC GROUP RES:{input_security_group}\n\n")
        return new_input_security_group


class MediaPackageV2Mixin(AWSBaseMixin):
    """Mixin for MediaPackageV2 operations."""

    mediapackage_channel_groups: list[MediaPackageV2ChannelGroup] = []

    @computed_field  # type: ignore[misc]
    @property
    def mediapackagev2(self) -> mediapackagev2Client:
        """Return a MediaPackageV2 boto3 client."""
        return self._boto_session.client("mediapackagev2")

    def create_mediapackagev2_channel_group(
        self,
        channel_group_name: str,
        description: Optional[str],
        tags: Optional[Mapping[str, str]],
    ) -> CreateChannelGroupResponseTypeDef:
        """Create a mediapackagev2 channel group."""
        if not self._boto_session:
            raise SendLiveError("Boto session not set up.")
        create_args: CreateChannelGroupRequestRequestTypeDef = {
            "ChannelGroupName": channel_group_name,
            "Tags": self.get_operation_tags(tags),
        }
        if description:
            create_args["Description"] = description
        mediapackagev2_channel_group: CreateChannelGroupResponseTypeDef = (
            self.mediapackagev2.create_channel_group(**create_args)
        )
        logger.info(
            f"\n\nMEDIAPACKAGEV2 CREATE CHANNEL GROUP RES:{mediapackagev2_channel_group}\n\n"
        )
        return mediapackagev2_channel_group

    def create_mediapackagev2_channel(
        self, channel_group_name: Optional[str], channel_name: str
    ) -> CreateChannelResponseTypeDef:
        """Create a mediapackagev2 channel.

        Defaults to creating the mediapackagev2 channel under the first mediapackagev2 channel group.
        """
        if not self._boto_session:
            raise SendLiveError("Boto session not set up.")
        if not channel_group_name and len(self.mediapackage_channel_groups) == 0:
            raise SendLiveError(
                "No mediapackagev2 channel groups are associated with this instance. Please add one to create a mediapackagev2 channel."
            )
        elif not channel_group_name:
            channel_group_name = self.mediapackage_channel_groups[0].name
        mediapackage_v2_channel: CreateChannelResponseTypeDef = (
            self.mediapackagev2.create_channel(
                ChannelGroupName=channel_group_name,
                ChannelName=channel_name,
                Tags=self.get_operation_tags(),
            )
        )
        logger.info(
            f"\n\nMEDIAPACKAGEV2 CREATE CHANNEL RES:{mediapackage_v2_channel}\n\n"
        )
        if (
            mediapackage_v2_channel["ResponseMetadata"]["HTTPStatusCode"]
            != HTTPStatus.CREATED
        ):
            raise SendLiveError(
                f"Failed to create mediapackagev2 channel, received non 201 created response: {mediapackage_v2_channel}"
            )
        if not channel_group_name:
            # No channel group name was provided, so we can safely add the newly created channel to the first channel group.
            new_mediapackagev2_channel: MediaPackageV2Channel = MediaPackageV2Channel(
                name=mediapackage_v2_channel["ChannelName"],
                arn=mediapackage_v2_channel["Arn"],
            )
            self.mediapackage_channel_groups[0].channels.append(
                new_mediapackagev2_channel
            )
            return mediapackage_v2_channel
        else:
            raise NotImplementedError(
                "Adding a channel to a specific channel group that may or may not be already associated with this instance is not yet implemented."
            )

    def create_mediapackagev2_origin_endpoint(
        self,
        channel_group_name: str,
        channel_name: str,
        origin_endpoint_name: str,
        container_type: ContainerTypeType,
    ) -> None:
        """Create a mediapackagev2 origin endpoint."""
        if not self._boto_session:
            raise SendLiveError("Boto session not set up.")
        mediapackagev2_origin_endpoint: CreateOriginEndpointResponseTypeDef = (
            self.mediapackagev2.create_origin_endpoint(
                ChannelGroupName=channel_group_name,
                ChannelName=channel_name,
                OriginEndpointName=origin_endpoint_name,
                ContainerType=container_type,
                Tags=self.get_operation_tags(),
            )
        )
        logger.info(
            f"\n\nMEDIAPACKAGEV2 CREATE ORIGIN ENDPOINT RES:{mediapackagev2_origin_endpoint}\n\n"
        )
        if (
            mediapackagev2_origin_endpoint["ResponseMetadata"]["HTTPStatusCode"]
            != HTTPStatus.CREATED
        ):
            raise SendLiveError(
                f"Failed to create mediapackagev2 origin endpoint, received non 201 created response: {mediapackagev2_origin_endpoint}"
            )
