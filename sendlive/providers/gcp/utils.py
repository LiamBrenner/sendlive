from google.cloud.video import live_stream_v1

from sendlive.providers.gcp.constants import (
    GCP_DEFAULT_720P_ES,
    GCP_DEFAULT_720P_MUX,
    GCP_DEFAULT_AUDIO_ES,
    GCP_DEFAULT_AUDIO_MUX,
    GCP_DEFAULT_MANIFEST,
)


def build_gcp_channel_obj_from_defaults(
    name: str, input_str: str, output_uri: str
) -> live_stream_v1.Channel:
    """Build a GCP channel object from defaults."""
    # TODO check relevance of input attachment key
    input_attachment = live_stream_v1.InputAttachment(
        key="input-attachment", input=input_str
    )
    output = live_stream_v1.Channel.Output(uri=output_uri)
    channel = live_stream_v1.Channel(
        name=name,
        input_attachments=[input_attachment],
        output=output,
        elementary_streams=[GCP_DEFAULT_720P_ES, GCP_DEFAULT_AUDIO_ES],
        mux_streams=[GCP_DEFAULT_720P_MUX, GCP_DEFAULT_AUDIO_MUX],
        manifests=[GCP_DEFAULT_MANIFEST],
    )
    return channel
