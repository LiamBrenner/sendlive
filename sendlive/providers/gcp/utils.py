from typing import Optional

from google.cloud.video import live_stream_v1

from sendlive.providers.gcp.constants import (
    GCP_DEFAULT_720P_ES,
    GCP_DEFAULT_720P_MUX,
    GCP_DEFAULT_AUDIO_ES,
    GCP_DEFAULT_AUDIO_MUX,
    GCP_DEFAULT_MANIFEST,
)
from sendlive.types import MappingTags


def build_gcp_channel_obj_from_defaults(
    name: str,
    input_str: str,
    bucket_output_uri: str,
    tags: Optional[MappingTags] = None,
) -> live_stream_v1.Channel:
    """Build a GCP channel object from defaults."""
    # TODO check relevance of input attachment key
    if tags is None:
        tags = dict()
    input_attachment = live_stream_v1.InputAttachment(
        key="input-attachment", input=input_str
    )
    bucket_uri_with_path = f"{bucket_output_uri}/sendlive/gcp-streams"
    output = live_stream_v1.Channel.Output(uri=bucket_uri_with_path)
    channel = live_stream_v1.Channel(
        name=name,
        input_attachments=[input_attachment],
        output=output,
        elementary_streams=[GCP_DEFAULT_720P_ES, GCP_DEFAULT_AUDIO_ES],
        mux_streams=[GCP_DEFAULT_720P_MUX, GCP_DEFAULT_AUDIO_MUX],
        manifests=[GCP_DEFAULT_MANIFEST],
        labels=tags or dict(),
    )
    return channel


def construct_gcp_base_name(project_id: str, location: str) -> str:
    """Construct the base name that makes up other specific GCP names."""
    return f"projects/{project_id}/locations/{location}"


def construct_gcp_input_endpoint_name(
    project_id: str, location: str, input_id: str
) -> str:
    """Construct an input endpoint name string for GCP."""
    return f"{construct_gcp_base_name(project_id, location)}/inputs/{input_id}"


def construct_gcp_channel_name(project_id: str, location: str, channel_id: str) -> str:
    """Construct a channel name string for GCP."""
    return f"{construct_gcp_base_name(project_id, location)}/channels/{channel_id}"
