# pytest
from bank import Bank

def test_import_works():
    """Test that Bank class can be imported and instantiated."""
    b = Bank()
    assert b is not None
    assert isinstance(b, Bank)

