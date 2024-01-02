from sendlive.utils import generate_dns_compliant_name


def test_generate_dns_compliant_name_returns_string_with_default_parameters() -> None:
    """Test that the generate_dns_compliant_name function returns a string when called with default parameters.

    The returned string should start with 'sendlive-' and contain four words separated by hyphens.
    """
    result = generate_dns_compliant_name()
    assert isinstance(result, str)
    assert result.startswith("sendlive-")
    assert len(result.split("-")) == 4


def test_generate_dns_compliant_name_returns_string_with_custom_prefix() -> None:
    """Test that the generate_dns_compliant_name function returns a string when called with a custom prefix.

    The returned string should start with the custom prefix and contain four words separated by hyphens.
    """
    result = generate_dns_compliant_name(prefix="custom")
    assert isinstance(result, str)
    assert result.startswith("custom-")
    assert len(result.split("-")) == 4


def test_generate_dns_compliant_name_returns_string_with_custom_num_words() -> None:
    """Test that the generate_dns_compliant_name function returns a string when called with a custom number of words.

    The returned string should start with 'sendlive-' and contain a number of words equal to the custom number plus two.
    """
    result = generate_dns_compliant_name(num_words=5)
    assert isinstance(result, str)
    assert result.startswith("sendlive-")
    assert len(result.split("-")) == 6
