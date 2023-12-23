from collections.abc import Mapping
from typing import Optional

from boto3.session import Session
from mypy_boto3_medialive import MediaLiveClient
from mypy_boto3_medialive.type_defs import (
    CreateInputSecurityGroupResponseTypeDef,
    InputSecurityGroupTypeDef,
)
from mypy_boto3_mediapackagev2 import mediapackagev2Client
from mypy_boto3_mediapackagev2.type_defs import (
    CreateChannelGroupRequestRequestTypeDef,
    CreateChannelGroupResponseTypeDef,
    CreateChannelResponseTypeDef,
)
from pydantic import ConfigDict, PrivateAttr, computed_field
from typing_extensions import override

from sendlive.adapter import BaseAdapter
from sendlive.constants import AWSCredentials, AWSOptions
from sendlive.exceptions import SendLiveError
from sendlive.logger import logger
from sendlive.providers.aws.mediapackage import (
    MediaPackageV2Channel,
    MediaPackageV2ChannelGroup,
)
from sendlive.providers.aws.stream import AWSStream


class AWSAdapter(BaseAdapter):
    """Adapter for AWS."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    credentials: AWSCredentials

    provider_options: Optional[AWSOptions] = None

    mediapackage_channel_groups: list[MediaPackageV2ChannelGroup] = []

    _boto_session: Session = PrivateAttr()

    @computed_field
    @property
    def medialive(self) -> MediaLiveClient:
        """Return a MediaLive client."""
        return self._boto_session.client("medialive")

    @computed_field
    @property
    def mediapackagev2(self) -> mediapackagev2Client:
        """Return a MediaLive client."""
        return self._boto_session.client("mediapackagev2")

    @override
    def setup_provider(self) -> None:
        self._boto_session = Session(
            aws_access_key_id=self.credentials.access_key,
            aws_secret_access_key=self.credentials.secret_key.get_secret_value(),
            region_name=self.credentials.region,
        )

    @override
    def setup_stream(self) -> None:
        return None

    @override
    def list_streams(self) -> list[str]:
        return list()

    @override
    def create_stream(
        self,
        name: str,
        input_security_group_id: Optional[int] = None,
        setup_endpoint: bool = True,
    ) -> AWSStream:
        if input_security_group_id is None:
            if (
                self.provider_options is None
                or self.provider_options.medialive_input_security_group_id is None
            ):
                input_security_group: InputSecurityGroupTypeDef = (
                    self.create_input_security_group()
                )
                input_security_group_id = int(input_security_group["Id"])
            else:
                input_security_group_id = (
                    self.provider_options.medialive_input_security_group_id
                )
        stream = AWSStream(name=name)
        if not self._boto_session:
            raise SendLiveError("Boto session not set up.")
        if setup_endpoint:
            stream.setup_endpoint(
                boto_session=self._boto_session,
                security_input_group_id=input_security_group_id,
            )
        return stream

    def create_input_security_group(self) -> InputSecurityGroupTypeDef:
        """Create a medialive input security group and return it."""
        if not self._boto_session:
            raise SendLiveError("Boto session not set up.")
        input_security_group: CreateInputSecurityGroupResponseTypeDef = (
            self.medialive.create_input_security_group(
                WhitelistRules=[{"Cidr": "0.0.0.0/0"}]
            )
        )
        if input_security_group["ResponseMetadata"]["HTTPStatusCode"] != 201:
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

    def create_mediapackage_channel_group(
        self,
        channel_group_name: str,
        description: Optional[str],
        tags: Optional[Mapping[str, str]],
    ) -> CreateChannelGroupResponseTypeDef:
        """Create a mediapackage channel group using mediapackagev2."""
        if not self._boto_session:
            raise SendLiveError("Boto session not set up.")
        create_args: CreateChannelGroupRequestRequestTypeDef = {
            "ChannelGroupName": channel_group_name
        }
        if description:
            create_args["Description"] = description
        if tags:
            create_args["Tags"] = tags
        mediapackagev2_channel_group: CreateChannelGroupResponseTypeDef = (
            self.mediapackagev2.create_channel_group(**create_args)
        )
        logger.info(
            f"\n\nMEDIAPACKAGEV2 CREATE CHANNEL GROUP RES:{mediapackagev2_channel_group}\n\n"
        )
        return mediapackagev2_channel_group

    def create_mediapackage_channel(
        self, channel_group_name: Optional[str], channel_name: str
    ) -> CreateChannelResponseTypeDef:
        """Create a mediapackage channel using mediapackagev2.

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
            )
        )
        logger.info(
            f"\n\nMEDIAPACKAGEV2 CREATE CHANNEL RES:{mediapackage_v2_channel}\n\n"
        )
        if mediapackage_v2_channel["ResponseMetadata"]["HTTPStatusCode"] != 201:
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
