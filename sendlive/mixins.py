from typing import Optional

from sendlive.constants import CREATED_BY_KEY, CREATED_BY_VALUE, DEFAULT_TAGS
from sendlive.types import MappingTags


class TagMixin:
    """Mixin adding operations to gather tags in different formats for tagging cloud provider resources."""

    @property
    def created_by_tag_key_lowercase_no_space(self) -> str:
        """Get the created by tag key in lowercase with no spaces."""
        return CREATED_BY_KEY.replace(" ", "-").lower()

    @property
    def created_by_tag_value_lowercase_no_space(self) -> str:
        """Get the created by tag value in lowercase with no spaces."""
        return CREATED_BY_VALUE.replace(" ", "-").lower()

    def get_operation_tags(
        self,
        tags: Optional[MappingTags] = None,
    ) -> MappingTags:
        """Ensure sendlive tags are inserted when tags are required for an operation - may be useful to override."""
        if not tags:
            return DEFAULT_TAGS
        return {**tags, **DEFAULT_TAGS}

    def get_operation_tags_lowercase_no_space_keys(
        self, tags: Optional[MappingTags] = None
    ) -> MappingTags:
        """Convert a mapping of tags to ensure all keys have no spaces and are lowercase. Spaces are replaced with hyphens."""
        tags = self.get_operation_tags(tags)

        return {key.replace(" ", "-").lower(): value for key, value in tags.items()}
