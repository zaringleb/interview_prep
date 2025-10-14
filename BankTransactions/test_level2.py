# pytest
from bank import Bank

def seed_transfers_for_metrics():
    b = Bank()
    for acc in ["A", "B", "C", "D"]:
        b.create_account(acc, 0)
    # fund senders
    b.deposit("A", 1000)
    b.deposit("B", 1000)
    b.deposit("C", 1000)
    # outgoing transfers
    b.transfer("A", "D", 300)   # A:300
    b.transfer("B", "D", 200)   # B:200
    b.transfer("C", "D", 100)   # C:100
    b.transfer("A", "D", 999)   # A:300+999=1299
    return b

def test_top_k_basic_and_partial():
    b = seed_transfers_for_metrics()
    # A is biggest spender (1299), then B (200), then C (100)
    assert b.top_k_by_outgoing(1) == ["A"]
    # ask for more than exist with activity
    assert b.top_k_by_outgoing(10) == ["A", "B", "C"]

def test_top_k_tie_break_lexicographic():
    b = Bank()
    for acc in ["A", "B", "X", "Y"]:
        b.create_account(acc, 0)
    for acc in ["A", "B"]:
        b.deposit(acc, 1000)
    # A and B each send 500 in total → tie; return lexicographically: ["A","B"]
    b.transfer("A", "X", 300)
    b.transfer("A", "X", 200)
    b.transfer("B", "Y", 500)
    assert b.top_k_by_outgoing(2) == ["A", "B"]

def test_top_k_ignores_deposits_and_empty_case():
    b = Bank()
    b.create_account("A", 0)
    b.deposit("A", 1000)  # no transfers
    assert b.top_k_by_outgoing(3) == []
