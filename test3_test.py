import pytest
from test_3 import calculate_average_price_per_sqft

def test_empty_input_does_not_crash():
    result = calculate_average_price_per_sqft([])
    assert result is None or result == 0

def test_correct_average():
    rows = [{"price": "200000", "sq__ft": "1000"}, {"price": "300000", "sq__ft": "1000"}]
    assert calculate_average_price_per_sqft(rows) == 250.0

def test_skips_invalid_and_zero_sqft_rows():
    rows = [
        {"price": "200000", "sq__ft": "1000"},
        {"price": "300000", "sq__ft": "0"},
        {"price": "abc", "sq__ft": "1000"},
        {"price": "400000", "sq__ft": "2000"}
    ]

    result = calculate_average_price_per_sqft(rows)

    assert result == 200.0