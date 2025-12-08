import pytest

from services.utils import parse_url


@pytest.mark.parametrize(
    "input_url,expected",
    [
        ("tehisintellekt.ee", "tehisintellekt.ee"),
        ("https://tehisintellekt.ee", "tehisintellekt.ee"),
        ("http://example.com", "example.com"),
        ("sven.spot", "sven.spot"),
        ("tehisintellekt.sven.spot", "tehisintellekt.sven.spot"),
        ("     www.neti.ee", "www.neti.ee"),
        ("https://www.google.com/search/howsearchworks/", "www.google.com"),
        (1, ""),
        (None, ""),
        ("x", ""),
        ("              ", ""),
    ],
)
def test_parse_url(input_url, expected):
    assert parse_url(input_url) == expected
