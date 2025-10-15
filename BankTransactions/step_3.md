## Step 3

From this step onwards, all events in the bank are timestamped. `deposit` and `transfer` methods now require a `timestamp` argument. All timestamps are integers and are guaranteed to be non-decreasing in the tests.

The new signatures are:
```python
deposit(self, account_id: str, amount: int, timestamp: int) -> int | None
transfer(self, from_id: str, to_id: str, amount: int, timestamp: int) -> int | None
```

---

Support transfers that execute at or before a future time. Executed scheduled transfers must be indistinguishable from manual transfers in metrics.

```python
schedule_transfer(self, from_id: str, to_id: str, amount: int, execute_at: int) -> str | None
```

Behavioral rules:
- `schedule_transfer` returns a non-empty string "schedule id" when the request is accepted, and `None` otherwise (e.g., invalid accounts, non-positive amount, or other invalid input). The returned id uniquely identifies the scheduled transfer.

Managing scheduled items:
```python
cancel_scheduled(self, schedule_id: str) -> bool
run_scheduled_until(self, timestamp: int) -> int
```
- `cancel_scheduled` removes the pending scheduled transfer with the given `schedule_id` and returns `True` if it existed and was removed; returns `False` if it did not exist (or was already executed/removed).
- `run_scheduled_until` executes all pending scheduled transfers with `execute_at <= timestamp` in time order. It returns the number of transfers that were successfully executed. All executed items are removed from the schedule. Any due item that fails at execution time (e.g., insufficient funds) must be removed without counting as executed.