from typing import Any, Optional

from google.api_core.exceptions import AlreadyExists
from google.api_core.operation import Operation
from google.cloud.storage import Bucket  # type: ignore
from google.cloud.storage import Client as StorageClient
from google.cloud.video.live_stream_v1 import Channel
from google.cloud.video.live_stream_v1 import Input as InputEndpoint
from google.cloud.video.live_stream_v1.services.livestream_service import (
    LivestreamServiceClient,
)
from google.oauth2.service_account import Credentials  # type: ignore
from google.protobuf.message import Message
from pydantic import BaseModel, ConfigDict, PrivateAttr

from sendlive.constants import (
    CREATED_BY_KEY,
    CREATED_BY_VALUE,
    GCPCredentials,
    GCPOptions,
)
from sendlive.exceptions import SendLiveError
from sendlive.logger import logger
from sendlive.mixins import TagMixin
from sendlive.providers.gcp.utils import build_gcp_channel_obj_from_defaults
from sendlive.types import MappingTags
from sendlive.utils import generate_dns_compliant_name


class GCPBaseMixin(BaseModel, TagMixin):
    """Base mixin for GCP operations."""

    _gcp_session: Credentials = PrivateAttr()
    _gcp_credentials: GCPCredentials = PrivateAttr()
    provider_options: Optional[GCPOptions] = GCPOptions()

    def get_tags(self, tags: Optional[MappingTags] = None) -> MappingTags:
        """Tags are referred to as labels in GCP land, and keys must not contain spaces."""
        return self.get_operation_tags_lowercase_no_space_keys(tags)

    def gcp_storage_client(self) -> StorageClient:
        """Create a google storage client."""
        return StorageClient(
            project=self._gcp_credentials.project_id, credentials=self._gcp_session
        )

    def gcp_live_streaming_api_client(self) -> LivestreamServiceClient:
        """Create a google live streaming api client."""
        return LivestreamServiceClient(credentials=self._gcp_session)

    def __init__(self, credentials: GCPCredentials, **data: dict[Any, Any]) -> None:
        """Set gcp session and credentials up."""
        super().__init__(credentials=credentials, **data)
        self._gcp_session = Credentials.from_service_account_info(
            info=credentials.service_account_json
        )
        self._gcp_credentials = credentials


class GCPCloudStorageMixin(GCPBaseMixin):
    """Mixin for GCP Cloud Storage operations."""

    _bucket: Bucket = PrivateAttr()

    def init_bucket(
        self, bucket_name: Optional[str] = None, tags: Optional[MappingTags] = None
    ) -> None:
        """Set instance gcp bucket up by either creating one, being supplied one, or finding an already created one."""
        if bucket_name is None and (
            self.provider_options is None or self.provider_options.bucket_name is None
        ):
            found_bucket_name = self.find_sendlive_metadata_tagged_bucket_name()
            if found_bucket_name is False:
                # User has not supplied a bucket name, and no pre-existing sendlive bucket was found - we'll create one now.
                new_bucket_name = generate_dns_compliant_name()
                logger.debug(
                    f"init_bucket: User did not supply bucket, and no pre-existing buckets found - creating a new bucket named {new_bucket_name}"
                )
                new_bucket = self.create_gcp_bucket(new_bucket_name, tags=tags)
                self._bucket = new_bucket
                return
            elif isinstance(found_bucket_name, str):
                found_bucket = self.get_gcp_bucket_with_name(found_bucket_name)
                logger.debug(
                    f"init_bucket: Found pre-existing sendlive bucket named {found_bucket.name} - using this bucket."
                )
                self._bucket = found_bucket
                return
        supplied_bucket = self.get_gcp_bucket_with_name(bucket_name)  # type: ignore
        logger.debug(
            f"init_bucket: User supplied bucket name {bucket_name} - using this bucket."
        )
        self._bucket = supplied_bucket
        return

    def get_gcp_bucket_with_name(self, bucket_name: str) -> Bucket:
        """Get a GCP bucket with the passed in name."""
        client = self.gcp_storage_client()
        return client.get_bucket(bucket_name)

    def find_sendlive_metadata_tagged_bucket_name(self) -> str | bool:
        """Search buckets by label to find gcp bucket name created for sendlive."""
        client = self.gcp_storage_client()
        buckets = client.list_buckets()

        found_buckets: list[str] = list()
        for bucket in buckets:
            if bucket.labels.get(CREATED_BY_KEY) == CREATED_BY_VALUE:
                found_buckets.append(bucket.name)
        if len(found_buckets) > 1:
            raise SendLiveError(
                f"Expected to find one bucket with label {CREATED_BY_KEY}:{CREATED_BY_VALUE}, instead found {len(found_buckets)}!"
            )
        elif len(found_buckets) == 0:
            return False
        return found_buckets[0]

    def add_tags_to_bucket(self, tags: Optional[MappingTags] = None) -> None:
        """Add tags to a GCP bucket."""
        tags_to_be_set: MappingTags = self.get_tags(tags)
        logger.debug(f"Setting tags on bucket {self._bucket.name}: {tags_to_be_set}")
        self._bucket.labels = tags_to_be_set
        self._bucket.patch()

    def create_gcp_bucket(
        self,
        bucket_name: str,
        storage_class: Optional[str] = "STANDARD",
        location: Optional[str] = "us",
        tags: Optional[MappingTags] = None,
    ) -> Bucket:
        """Create a GCP bucket, and add tags to it."""
        storage_client = self.gcp_storage_client()
        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = storage_class
        sendlive_bucket = storage_client.create_bucket(bucket, location=location)
        logger.info(f"\nGCP Create bucket res:{sendlive_bucket}\n\n")
        self._bucket = sendlive_bucket
        self.add_tags_to_bucket(tags)
        return sendlive_bucket


class GCPLiveStreamAPIMixin(GCPBaseMixin):
    """Mixin for GCP Live Streaming API operations."""

    gcp_input_endpoints: list[InputEndpoint] = []

    gcp_channels: list[Channel] = []

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_input_endpoint(
        self, input_id: str, add_to_self: bool = False
    ) -> InputEndpoint:
        """Get a GCP input endpoint."""
        parent = f"projects/{self._gcp_credentials.project_id}/locations/{self._gcp_credentials.region}"
        input_str = f"{parent}/inputs/{input_id}"
        input_endpoint = self.gcp_live_streaming_api_client().get_input(name=input_str)
        if add_to_self:
            self.gcp_input_endpoints.extend([input_endpoint])
        return input_endpoint

    def create_input_endpoint(
        self,
        input_id: str,
        input_type: str = "RTMP_PUSH",
        get_if_exists: bool = True,
        tags: Optional[MappingTags] = None,
    ) -> InputEndpoint:
        """Create a GCP input endpoint.

        This operation appears to take a decent amount of time to complete.
        It may be advisable to use a library such as celery when invoking.

        Args:
        ----
            input_id (str): The ID of the input.
            input_type (str, optional): The type of the input. Defaults to "RTMP_PUSH".
            get_if_exists (bool, optional): If True, fetches the input with the passed in input_id if an already exists error is returned by GCP. Defaults to True.
            tags (Optional[MappingTags], optional): The tags for the input. Defaults to None.

        Returns:
        -------
            InputEndpoint: The created input endpoint.
        """
        parent = f"projects/{self._gcp_credentials.project_id}/locations/{self._gcp_credentials.region}"
        input_endpoint = InputEndpoint(type_=input_type, labels=self.get_tags(tags))
        try:
            operation: Operation = self.gcp_live_streaming_api_client().create_input(
                parent=parent, input=input_endpoint, input_id=input_id
            )
        except AlreadyExists as e:
            if get_if_exists:
                return self.get_input_endpoint(input_id, add_to_self=True)
            else:
                raise e
        response: Message = operation.result(900)  # type: ignore
        logger.info(f"\nGCP Create input endpoint res:{response}\n\n")

        if not isinstance(response, InputEndpoint):
            raise SendLiveError(
                f"Unexpected response from GCP - Create input endpoint response not of type InputEndpoint: {response}"
            )
        self.gcp_input_endpoints.extend([response])
        return response

    def create_channel(
        self,
        input_id: str,
        channel_id: str,
        tags: Optional[MappingTags] = None,
    ) -> Channel:
        """Create a GCP channel."""
        parent = f"projects/{self._gcp_credentials.project_id}/locations/{self._gcp_credentials.region}"
        input_str = f"{parent}/inputs/{input_id}"
        name = f"{parent}/channels/{channel_id}"
        channel: Channel = build_gcp_channel_obj_from_defaults(
            name,
            input_str,
            f"gs://{self.gcp_input_endpoints[0].uri}",
            tags=self.get_tags(tags),
        )
        operation: Operation = self.gcp_live_streaming_api_client().create_channel(
            parent=parent, channel=channel, channel_id=channel_id
        )
        response: Message = operation.result(600)  # type: ignore
        logger.info(f"\nGCP Create channel res:{response}\n\n")

        if not isinstance(response, Channel):
            raise SendLiveError(
                f"Unexpected response from GCP - Create channel response not of type Channel: {response}"
            )
        return response
