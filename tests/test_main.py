"""Unit tests for py-nuban"""

import sys
from pathlib import Path

# Add src to path for development testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from py_nuban import get_possible_banks, get_set_of_possible_codes


def test_get_possible_banks_valid():
    """Test get_possible_banks with a valid account number."""
    result = get_possible_banks("1901880678")
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)
    print(f"Test passed. Possible banks for 1901880678: {result}")


def test_get_possible_banks_invalid_length():
    """Test that invalid lengths raise ValueError."""
    try:
        get_possible_banks("123")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"Test passed. Correctly raised: {e}")


def test_get_possible_banks_invalid_type():
    """Test that non-string input raises TypeError."""
    try:
        get_possible_banks(1901880678)
        assert False, "Should have raised TypeError"
    except TypeError as e:
        print(f"Test passed. Correctly raised: {e}")


def test_get_possible_banks_non_digit():
    """Test that non-digit characters raise ValueError."""
    try:
        get_possible_banks("190188067a")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"Test passed. Correctly raised: {e}")

def test_get_set_of_possible_codes_valid():
    """Test get_set_of_possible_codes with a valid account number."""
    result = get_set_of_possible_codes("1901880678")
    assert isinstance(result, set)
    print(f"Test passed. Possible codes for 1901880678: {result}")

def test_get_set_of_possible_codes_invalid_length():
    """Test that invalid lengths raise ValueError."""
    try:
        get_set_of_possible_codes("123")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"Test passed. Correctly raised: {e}")

def test_get_set_of_possible_codes_non_digit():
    """Test that non-digit characters raise ValueError."""
    try:
        get_set_of_possible_codes("190188067a")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"Test passed. Correctly raised: {e}")
        
def test_get_set_of_possible_banks_invalid_type():
    """Test that non-string input raises TypeError."""
    try:
        get_set_of_possible_codes(1901880678)
        assert False, "Should have raised TypeError"
    except TypeError as e:
        print(f"Test passed. Correctly raised: {e}")

if __name__ == "__main__":
    test_get_possible_banks_valid()
    test_get_possible_banks_invalid_length()
    test_get_possible_banks_invalid_type()
    test_get_possible_banks_non_digit()

    test_get_set_of_possible_codes_valid()
    test_get_set_of_possible_codes_invalid_length()
    test_get_set_of_possible_codes_non_digit()
    test_get_set_of_possible_banks_invalid_type()
    print("\nAll tests passed!")
