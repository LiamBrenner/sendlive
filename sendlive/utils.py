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
