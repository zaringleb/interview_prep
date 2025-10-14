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