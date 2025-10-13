# pytest
from bank import Bank

def setup_merge_fixture():
    b = Bank()
    for acc in ["A", "B", "C"]:
        b.create_account(acc, 0)
    b.deposit("A", 500, 1)
    b.deposit("B", 700, 1)
    b.deposit("C", 0, 1)
    # some pre-merge activity
    b.transfer("A", "C", 200, 10)  # A->C
    return b

def test_merge_success_and_closing_of_sources():
    b = setup_merge_fixture()
    merged_balance = b.merge_accounts("A", "B", "M", 25)
    #  A has 300 left (500 - 200 sent), B has 700 → merged 1000
    assert merged_balance == 1000

    # sources closed for writes
    assert b.deposit("A", 1, 30) is None
    assert b.transfer("A", "C", 1, 31) is None
    assert b.transfer("C", "A", 1, 31) is None

    # merged account is usable
    assert b.deposit("M", 50, 32) == 1050
    assert b.transfer("M", "C", 20, 33) == 1030

def test_merge_repoints_pending_schedules_and_executes_from_merged():
    b = setup_merge_fixture()
    # schedule: A -> C at t=40; will be pending at merge time t=25
    sid = b.schedule_transfer("A", "C", 100, 40)
    assert sid

    merged_balance = b.merge_accounts("A", "B", "M", 25)
    assert merged_balance == 1000

    # when we run, the transfer should execute FROM M (A is closed)
    executed = b.run_scheduled_until(100)
    assert executed == 1
    # balances reflect M->C rather than A->C
    # Before executing schedule: M balance = 1000
    assert b.get_balance("M") == 900
    assert b.get_balance("C") == 200 + 100  # pre-merge + scheduled

def test_get_statement_counts_history_by_original_ids():
    b = setup_merge_fixture()
    # A had one transfer pre-merge; B had none
    assert b.get_statement("A", 0, 100) == 1
    assert b.get_statement("B", 0, 100) == 0

    # merge, then do a new transfer from M
    b.merge_accounts("A", "B", "M", 25)
    b.transfer("M", "C", 10, 60)

    # A's historical count stays 1; M only sees post-merge activity
    assert b.get_statement("A", 0, 100) == 1
    assert b.get_statement("M", 0, 100) >= 1  # at least the post-merge transfer
