class Bank():
    def __init__(self):
        self._balances = {}
        self._transactions = []
        # Scheduled transfers: id -> item dict
        self._scheduled = {}
        self._schedule_seq = 0

    def create_account(self, account_id: str, initial_balance: int) -> bool:
        if not isinstance(account_id, str) or account_id == "":
            return False
        if account_id in self._balances:
            return False
        self._balances[account_id] = int(initial_balance)
        return True

    def deposit(self, account_id: str, amount: int, timestamp: int):
        if account_id not in self._balances:
            return None
        if not isinstance(amount, int) or amount <= 0:
            return None
        # Apply deposit
        self._balances[account_id] += amount
        # Log transaction
        self._transactions.append({
            "type": "deposit",
            "account_id": account_id,
            "amount": amount,
            "timestamp": int(timestamp),
        })
        return self._balances[account_id]

    def transfer(self, from_id: str, to_id: str, amount: int, timestamp: int):
        if from_id not in self._balances or to_id not in self._balances:
            return None
        if not isinstance(amount, int) or amount <= 0:
            return None
        if self._balances[from_id] < amount:
            return None
        # Apply transfer atomically
        self._balances[from_id] -= amount
        self._balances[to_id] += amount
        # Log transaction
        self._transactions.append({
            "type": "transfer",
            "from_id": from_id,
            "to_id": to_id,
            "amount": amount,
            "timestamp": int(timestamp),
        })
        return self._balances[from_id]

    def get_balance(self, account_id: str):
        if account_id not in self._balances:
            return None
        return self._balances[account_id]

    def top_k_by_outgoing(self, start_ts: int, end_ts: int, k: int) -> list[str]:
        if not isinstance(k, int) or k <= 0:
            return []
        if start_ts > end_ts:
            return []

        totals_by_sender = {}
        for tx in self._transactions:
            if tx.get("type") != "transfer":
                continue
            ts = tx.get("timestamp")
            if ts is None or ts < start_ts or ts > end_ts:
                continue
            sender = tx.get("from_id")
            amount = tx.get("amount", 0)
            if not isinstance(amount, int) or amount <= 0:
                continue
            totals_by_sender[sender] = totals_by_sender.get(sender, 0) + amount

        if not totals_by_sender:
            return []

        ranked = sorted(totals_by_sender.items(), key=lambda item: (-item[1], item[0]))
        return [account_id for account_id, _ in ranked[:k]]

    def schedule_transfer(self, from_id: str, to_id: str, amount: int, execute_at: int) -> str | None:
        if from_id not in self._balances or to_id not in self._balances:
            return None
        if not isinstance(amount, int) or amount <= 0:
            return None
        schedule_id = f"s{self._schedule_seq}"
        self._schedule_seq += 1
        self._scheduled[schedule_id] = {
            "from_id": from_id,
            "to_id": to_id,
            "amount": int(amount),
            "execute_at": int(execute_at),
            "seq": self._schedule_seq,
        }
        return schedule_id

    def cancel_scheduled(self, schedule_id: str) -> bool:
        if schedule_id in self._scheduled:
            del self._scheduled[schedule_id]
            return True
        return False

    def run_scheduled_until(self, timestamp: int) -> int:
        # Collect items to execute now, in nondecreasing time order
        ready = []
        for sid, item in self._scheduled.items():
            if item.get("execute_at", 0) <= timestamp:
                ready.append((item["execute_at"], item.get("seq", 0), sid, item))

        if not ready:
            return 0

        ready.sort(key=lambda t: (t[0], t[1]))

        executed_count = 0
        for execute_at, _seq, sid, item in ready:
            # Remove from scheduled regardless of success (no retry on failure)
            if sid in self._scheduled:
                del self._scheduled[sid]
            result = self.transfer(item["from_id"], item["to_id"], item["amount"], execute_at)
            if result is not None:
                executed_count += 1
        return executed_count

    def merge_accounts(self, a_id: str, b_id: str, merged_id: str, timestamp: int) -> int | None:
        # Preconditions
        if not isinstance(a_id, str) or not isinstance(b_id, str) or not isinstance(merged_id, str):
            return None
        if a_id == b_id or a_id == merged_id or b_id == merged_id:
            return None
        if a_id not in self._balances or b_id not in self._balances:
            return None
        if merged_id in self._balances:
            return None

        # Compute merged balance at the given timestamp
        merged_balance = int(self._balances[a_id]) + int(self._balances[b_id])

        # Create the merged account with computed balance
        self._balances[merged_id] = merged_balance

        # Repoint any pending scheduled items referencing a_id or b_id to merged_id
        for _sid, item in self._scheduled.items():
            if item.get("from_id") in (a_id, b_id):
                item["from_id"] = merged_id
            if item.get("to_id") in (a_id, b_id):
                item["to_id"] = merged_id

        # Close source accounts by removing them from active balances
        if a_id in self._balances:
            del self._balances[a_id]
        if b_id in self._balances:
            del self._balances[b_id]

        # Append merge record to transaction log
        self._transactions.append({
            "type": "merge",
            "a_id": a_id,
            "b_id": b_id,
            "merged_id": merged_id,
            "timestamp": int(timestamp),
        })

        return merged_balance

    def get_statement(self, account_id: str, start_ts: int, end_ts: int) -> int | None:
        # Validate window
        if not isinstance(start_ts, int) or not isinstance(end_ts, int):
            return None
        if start_ts > end_ts:
            return 0

        count = 0
        has_history = False

        for tx in self._transactions:
            ts = tx.get("timestamp")
            tx_type = tx.get("type")

            # Track whether the account has any historical presence at all
            if tx_type == "transfer":
                if account_id == tx.get("from_id") or account_id == tx.get("to_id"):
                    has_history = True
            elif tx_type == "deposit":
                if account_id == tx.get("account_id"):
                    has_history = True
            elif tx_type == "merge":
                if account_id == tx.get("merged_id"):
                    has_history = True

            # Count only transfers (as sender/receiver) within the window, plus the merge record for merged_id
            if ts is None or ts < start_ts or ts > end_ts:
                continue

            if tx_type == "transfer":
                if account_id == tx.get("from_id") or account_id == tx.get("to_id"):
                    count += 1
            elif tx_type == "merge":
                if account_id == tx.get("merged_id"):
                    count += 1

        if count > 0:
            return count

        # No matching events in window; return 0 if account currently exists or has any history, else None
        if account_id in self._balances or has_history:
            return 0
        return None