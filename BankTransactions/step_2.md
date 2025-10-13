Add a metric over your transaction log. Do not change Level-1 behavior.

top_k_by_outgoing(self, start_ts: int, end_ts: int, k: int) -> list[str]
Consider only "transfer" records sent by each account with start_ts ≤ timestamp ≤ end_ts.
For each account, sum outgoing amounts in that range.
Return up to k account IDs sorted by descending total; break ties by lexicographic account_id ascending.
Return an empty list if no account sent money in range.