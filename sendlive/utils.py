import random
from typing import Optional

from faker import Faker

from sendlive.adapter import BaseAdapter
from sendlive.constants import ServiceProvider


def get_adapter_for_provider(
    provider: ServiceProvider,
) -> type[BaseAdapter]:
    """Return the adapter class for the given provider."""
    if provider == ServiceProvider.AWS:
        from sendlive.providers.aws.adapter import AWSAdapter

        return AWSAdapter
    if provider == ServiceProvider.GCP:
        from sendlive.providers.gcp.adapter import GCPAdapter

        return GCPAdapter
    raise NotImplementedError(f"Provider {provider} is not supported.")


def generate_dns_compliant_name(
    prefix: Optional[str] = "sendlive", num_words: Optional[int] = 3
) -> str:
    """Generate a DNS compliant name suitable for S3/GCP bucket names for example.

    You may optionally include a string that the generated name should contain.
    """
    faker = Faker()
    words = faker.words(num_words)

    # TODO ensure prefix cannot make the returned string not DNS compliant
    return f'{prefix}-{"-".join(random.sample(words, len(words)))}'
