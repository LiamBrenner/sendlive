from sendlive import SendLive
from sendlive.constants import AWSCredentials


def start_stream() -> None:
    """Sendlive demo - starting a stream."""
    sl_aws_cred = AWSCredentials(
        access_key="fake",
        secret_key="fake",  # noqa: S106
        region="ap-southeast-2",
    )
    sl = SendLive(credentials=sl_aws_cred)
    print(sl)
