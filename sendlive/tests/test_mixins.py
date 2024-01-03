import pytest

from sendlive.mixins import TagMixin


class TestTagMixin:
    """Test cases for the TagMixin class."""

    @pytest.fixture
    def mixin(self) -> TagMixin:
        """Fixture that returns an instance of TagMixin."""
        return TagMixin()

    def test_created_by_tag_key_lowercase_no_space(self, mixin: TagMixin) -> None:
        """Test if the created_by_tag_key_lowercase_no_space property returns the expected string."""
        expected: str = "created-by"
        assert mixin.created_by_tag_key_lowercase_no_space == expected

    def test_created_by_tag_value_lowercase_no_space(self, mixin: TagMixin) -> None:
        """Test if the created_by_tag_value_lowercase_no_space property returns the expected string."""
        expected: str = "sendlive"
        assert mixin.created_by_tag_value_lowercase_no_space == expected

    def test_get_operation_tags_with_no_args(self, mixin: TagMixin) -> None:
        """Test get_operation_tags method with no arguments."""
        expected: dict[str, str] = {"Created By": "sendlive"}
        assert mixin.get_operation_tags() == expected

    def test_get_operation_tags_with_additional_tags(self, mixin: TagMixin) -> None:
        """Test get_operation_tags method with additional tags."""
        additional_tags: dict[str, str] = {"Environment": "Production"}
        expected: dict[str, str] = {
            "Created By": "sendlive",
            "Environment": "Production",
        }
        assert mixin.get_operation_tags(additional_tags) == expected

    def test_get_operation_tags_lowercase_no_space_keys_with_no_args(
        self, mixin: TagMixin
    ) -> None:
        """Test get_operation_tags_lowercase_no_space_keys method with no arguments."""
        expected: dict[str, str] = {"created-by": "sendlive"}
        assert mixin.get_operation_tags_lowercase_no_space_keys() == expected

    def test_get_operation_tags_lowercase_no_space_keys_with_additional_tags(
        self, mixin: TagMixin
    ) -> None:
        """Test get_operation_tags_lowercase_no_space_keys method with additional tags."""
        additional_tags: dict[str, str] = {
            "Environment": "Production",
            "Service Name": "API",
        }
        expected: dict[str, str] = {
            "created-by": "sendlive",
            "environment": "Production",
            "service-name": "API",
        }
        assert (
            mixin.get_operation_tags_lowercase_no_space_keys(additional_tags)
            == expected
        )
