Support transfers that execute at or before a future time. Executed scheduled transfers must be indistinguishable from manual transfers in metrics.

schedule_transfer(self, from_id: str, to_id: str, amount: int, execute_at: int) -> str | None
Create a pending transfer to run at execute_at.
Returns a unique schedule_id on success; None if from_id/to_id unknown or amount <= 0.

cancel_scheduled(self, schedule_id: str) -> bool
Cancel a pending item that has not executed.
Returns True if canceled; False if unknown or not pending.

run_scheduled_until(self, timestamp: int) -> int
Execute all pending items with execute_at ≤ timestamp in nondecreasing time order.
Each execution behaves exactly like transfer(..., timestamp=execute_at).
If funds are insufficient at execution, mark the item failed and remove it (no retry).
Returns the count of successfully executed items.