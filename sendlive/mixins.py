from collections.abc import Mapping, Sequence
from typing import Optional

from sendlive.constants import DEFAULT_TAGS


class TagMixin:
    """Mixin adding operations to gather tags in different formats for tagging cloud provider resources."""

    def get_operation_tags(
        self,
        tags: Optional[Mapping[str, str]] = {},
    ) -> Mapping[str, str]:
        """Ensure sendlive tags are inserted when tags are required for an operation - may be useful to override."""
        if not tags:
            return DEFAULT_TAGS
        return {**tags, **DEFAULT_TAGS}

    def get_operation_tags_as_sequence_tuple(
        self, tags: Mapping[str, str] = {}
    ) -> Sequence[tuple[str, str]]:
        """Convert a mapping of tags to a sequence of tuples."""
        tags = self.get_operation_tags(tags)

        return [(key, value) for key, value in tags.items()]
