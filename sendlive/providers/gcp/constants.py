from google.cloud.video import live_stream_v1
from google.protobuf import duration_pb2 as duration

### GCP Channel Defaults ###

## Elementary Stream Defaults ##

GCP_DEFAULT_720P_ES = live_stream_v1.ElementaryStream(
    key="es_video_720p",
    video_stream=live_stream_v1.VideoStream(
        h264=live_stream_v1.VideoStream.H264CodecSettings(
            profile="high",
            width_pixels=1280,
            height_pixels=720,
            bitrate_bps=3000000,
            frame_rate=30,
        )
    ),
)

GCP_DEFAULT_AUDIO_ES = live_stream_v1.ElementaryStream(
    key="es_audio",
    audio_stream=live_stream_v1.AudioStream(
        codec="aac", channel_count=2, bitrate_bps=160000
    ),
)

## Mux Stream Defaults ##

GCP_DEFAULT_720P_MUX = live_stream_v1.MuxStream(
    key="mux_video_720p",
    elementary_streams=["es_video_720p"],
    segment_settings=live_stream_v1.SegmentSettings(
        segment_duration=duration.Duration(
            seconds=2,
        ),
    ),
)

GCP_DEFAULT_AUDIO_MUX = live_stream_v1.MuxStream(
    key="mux_audio",
    elementary_streams=["es_audio"],
    segment_settings=live_stream_v1.SegmentSettings(
        segment_duration=duration.Duration(
            seconds=2,
        ),
    ),
)

## Other channel defaults ##

GCP_DEFAULT_MANIFEST = live_stream_v1.Manifest(
    file_name="manifest.m3u8",
    type_="HLS",
    mux_streams=["mux_video_720p", "mux_audio"],
    max_segment_count=5,
)
