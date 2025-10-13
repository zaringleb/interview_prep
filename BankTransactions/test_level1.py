# pytest
from bank import Bank

def test_create_account_basic_and_duplicate():
    b = Bank()
    assert b.create_account("A", 1000) is True
    assert b.create_account("A", 0) is False  # duplicate

def test_get_balance_unknown_and_known():
    b = Bank()
    assert b.get_balance("X") is None
    b.create_account("A", 123)
    assert b.get_balance("A") == 123

def test_deposit_success_and_failures():
    b = Bank()
    b.create_account("A", 0)
    assert b.deposit("A", 500, 10) == 500
    # negative / zero amounts invalid
    assert b.deposit("A", 0, 11) is None
    assert b.deposit("A", -1, 12) is None
    # unknown account
    assert b.deposit("Z", 10, 13) is None

def test_transfer_success_and_errors():
    b = Bank()
    b.create_account("A", 1000)
    b.create_account("B", 10)
    # insufficient funds
    assert b.transfer("B", "A", 1000, 10) is None
    # unknown accounts
    assert b.transfer("C", "A", 1, 11) is None
    assert b.transfer("A", "C", 1, 12) is None
    # valid transfer returns new balance of sender
    new_bal = b.transfer("A", "B", 250, 20)
    assert new_bal == 750
    assert b.get_balance("A") == 750 and b.get_balance("B") == 260
