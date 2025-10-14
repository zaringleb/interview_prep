## Step 2

Add a metric over your transaction log.

```python
top_k_by_outgoing(self, k: int) -> list[str]
```
Consider all "transfer" records sent by each account.
For each account, sum all outgoing amounts.
Return up to k account IDs sorted by descending total; break ties by lexicographic account_id ascending.
Return an empty list if no account has sent any money.