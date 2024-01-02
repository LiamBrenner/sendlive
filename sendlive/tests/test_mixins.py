from unittest.mock import patch

import pytest

from sendlive.mixins import TagMixin


class TestTagMixin:
    """Test cases for TagMixin."""

    @pytest.fixture
    def tag_mixin(self) -> TagMixin:
        """Fixture for creating TagMixin instance."""
        return TagMixin()

    def test_created_by_tag_key_lowercase_no_space(self, tag_mixin: TagMixin) -> None:
        """Test if created_by_tag_key_lowercase_no_space property returns the expected value."""
        with patch.object(
            TagMixin, "CREATED_BY_KEY", new_callable=property
        ) as mock_key:
            mock_key.return_value = "Test Key"
            assert tag_mixin.created_by_tag_key_lowercase_no_space == "test-key"

    def test_created_by_tag_value_lowercase_no_space(self, tag_mixin: TagMixin) -> None:
        """Test if created_by_tag_value_lowercase_no_space property returns the expected value."""
        with patch.object(
            TagMixin, "CREATED_BY_VALUE", new_callable=property
        ) as mock_value:
            mock_value.return_value = "Test Value"
            assert tag_mixin.created_by_tag_value_lowercase_no_space == "test-value"

    def test_get_operation_tags(self, tag_mixin: TagMixin) -> None:
        """Test if get_operation_tags method returns the expected value."""
        with patch.object(TagMixin, "DEFAULT_TAGS", new_callable=property) as mock_tags:
            mock_tags.return_value = {"tag1": "value1"}
            assert tag_mixin.get_operation_tags() == {"tag1": "value1"}
            assert tag_mixin.get_operation_tags({"tag2": "value2"}) == {
                "tag1": "value1",
                "tag2": "value2",
            }

    def test_get_operation_tags_lowercase_no_space_keys(
        self, tag_mixin: TagMixin
    ) -> None:
        """Test if get_operation_tags_lowercase_no_space_keys method returns the expected value."""
        with patch.object(TagMixin, "get_operation_tags") as mock_get_tags:
            mock_get_tags.return_value = {"Test Key": "value1"}
            assert tag_mixin.get_operation_tags_lowercase_no_space_keys() == {
                "test-key": "value1"
            }
