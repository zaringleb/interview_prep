## Step 4

Enable consolidation of two accounts into a new one, keeping historical identity for queries.

```python
merge_accounts(self, a_id: str, b_id: str, merged_id: str, timestamp: int) -> int | None
```
Preconditions: a_id and b_id exist; merged_id does not exist; all three IDs are distinct.
Create merged_id at timestamp with balance balance(a_id) + balance(b_id).
After merge, a_id and b_id become closed for future writes (deposit, transfer, scheduling).
Any pending scheduled item referencing a_id or b_id must be repointed to merged_id (same role: from/to).
Append a "merge" record to your log.
Returns the balance of merged_id on success; None on failure.

```python
get_statement(self, account_id: str, start_ts: int, end_ts: int) -> int | None
```
Count transactions in which account_id participated at the time (sender or receiver) with start_ts ≤ ts ≤ end_ts.
Returns that count; returns None only if account_id has no history and does not exist.
History rule: pre-merge transfers remain attributed to the original IDs (a_id/b_id); merged_id accrues activity only from the merge onward (plus the merge record itself).