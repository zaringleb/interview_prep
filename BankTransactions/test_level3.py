# pytest
from bank import Bank

def base_bank_with_funds():
    b = Bank()
    for acc in ["A", "B", "C"]:
        b.create_account(acc, 0)
    b.deposit("A", 1000, 1)
    b.deposit("B", 1000, 1)
    return b

def test_schedule_and_cancel():
    b = base_bank_with_funds()
    sid = b.schedule_transfer("A", "B", 300, 50)
    assert isinstance(sid, str) and sid
    assert b.cancel_scheduled(sid) is True
    # second cancel should fail
    assert b.cancel_scheduled(sid) is False

def test_run_scheduled_executes_in_time_order_and_affects_balances():
    b = base_bank_with_funds()
    sid1 = b.schedule_transfer("A", "B", 200, 10)
    sid2 = b.schedule_transfer("A", "C", 300, 5)
    sid3 = b.schedule_transfer("B", "C", 100, 10)
    assert all(isinstance(s, str) and s for s in [sid1, sid2, sid3])

    # execute all up to t=10 (sid2 @5, sid1 @10, sid3 @10)
    executed = b.run_scheduled_until(10)
    assert executed == 3
    # balances reflect all three transfers
    assert b.get_balance("A") == 1000 - 200 - 300
    assert b.get_balance("B") == 1000 - 100 + 200
    assert b.get_balance("C") == 300 + 100

def test_run_scheduled_handles_insufficient_funds_without_crashing():
    b = base_bank_with_funds()
    # drain A so scheduled will fail later
    assert b.transfer("A", "B", 1000, 2) == 0
    sid = b.schedule_transfer("A", "C", 1, 5)
    assert sid
    executed = b.run_scheduled_until(10)
    assert executed == 0
    # nothing executed; item removed (running again executes nothing)
    assert b.run_scheduled_until(100) == 0
