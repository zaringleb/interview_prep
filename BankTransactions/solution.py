class Bank():
    def __init__(self):
        self.accounts = {}  # account_id -> balance
        self.transaction_log = []  # list of transaction records
        self.scheduled_transfers = {}  # schedule_id -> scheduled transfer info
        self.next_schedule_id = 1  # counter for generating unique schedule IDs
        self.closed_accounts = set()  # accounts that have been merged and are closed for writes
    
    def create_account(self, account_id: str, initial_balance: int) -> bool:
        """Create account with starting balance.
        Returns True if created; False if account_id already exists.
        """
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = initial_balance
        return True
    
    def deposit(self, account_id: str, amount: int, timestamp: int = 0) -> int | None:
        """Increase balance by amount (must be > 0).
        Returns the new balance on success; None if account is unknown or amount <= 0.
        """
        if account_id not in self.accounts or amount <= 0:
            return None
        # Check if account is closed (merged)
        if account_id in self.closed_accounts:
            return None
        self.accounts[account_id] += amount
        self.transaction_log.append({
            'type': 'deposit',
            'account_id': account_id,
            'amount': amount,
            'timestamp': timestamp
        })
        return self.accounts[account_id]
    
    def transfer(self, from_id: str, to_id: str, amount: int, timestamp: int = 0) -> int | None:
        """Atomically move funds from from_id to to_id.
        Returns the new balance of from_id on success; None on failure.
        """
        # Check if both accounts exist
        if from_id not in self.accounts or to_id not in self.accounts:
            return None
        # Check if either account is closed (merged)
        if from_id in self.closed_accounts or to_id in self.closed_accounts:
            return None
        # Check if amount is valid
        if amount <= 0:
            return None
        # Check if from_id has sufficient funds
        if self.accounts[from_id] < amount:
            return None
        # Perform the transfer atomically
        self.accounts[from_id] -= amount
        self.accounts[to_id] += amount
        self.transaction_log.append({
            'type': 'transfer',
            'from_id': from_id,
            'to_id': to_id,
            'amount': amount,
            'timestamp': timestamp
        })
        return self.accounts[from_id]
    
    def get_balance(self, account_id: str) -> int | None:
        """Returns current balance; None if account unknown."""
        if account_id not in self.accounts:
            return None
        return self.accounts[account_id]
    
    def top_k_by_outgoing(self, k: int) -> list[str]:
        """Return up to k account IDs sorted by descending total outgoing transfers.
        Ties are broken by lexicographic account_id ascending.
        Returns empty list if no account has sent any money.
        """
        # Calculate total outgoing for each account
        outgoing_totals = {}
        for transaction in self.transaction_log:
            if transaction['type'] == 'transfer':
                from_id = transaction['from_id']
                amount = transaction['amount']
                outgoing_totals[from_id] = outgoing_totals.get(from_id, 0) + amount
        
        # If no transfers, return empty list
        if not outgoing_totals:
            return []
        
        # Sort by descending total, then by account_id ascending for ties
        sorted_accounts = sorted(outgoing_totals.items(), 
                                key=lambda x: (-x[1], x[0]))
        
        # Return up to k account IDs
        return [account_id for account_id, _ in sorted_accounts[:k]]
    
    def schedule_transfer(self, from_id: str, to_id: str, amount: int, execute_at: int) -> str | None:
        """Schedule a transfer to execute at or before a future time.
        Returns a unique schedule ID on success; None on failure.
        """
        # Basic validation - check if accounts exist
        if from_id not in self.accounts or to_id not in self.accounts:
            return None
        # Check if either account is closed (merged)
        if from_id in self.closed_accounts or to_id in self.closed_accounts:
            return None
        if amount <= 0:
            return None
        
        # Generate unique schedule ID
        schedule_id = f"schedule_{self.next_schedule_id}"
        self.next_schedule_id += 1
        
        # Store the scheduled transfer
        self.scheduled_transfers[schedule_id] = {
            'from_id': from_id,
            'to_id': to_id,
            'amount': amount,
            'execute_at': execute_at
        }
        
        return schedule_id
    
    def cancel_scheduled(self, schedule_id: str) -> bool:
        """Cancel a scheduled transfer.
        Returns True if successfully canceled; False if doesn't exist or already canceled.
        """
        if schedule_id in self.scheduled_transfers:
            del self.scheduled_transfers[schedule_id]
            return True
        return False
    
    def run_scheduled_until(self, timestamp: int) -> int:
        """Execute all scheduled transfers at or before the given timestamp.
        Scheduled transfers are executed in time order.
        Returns the count of successfully executed transfers.
        """
        # Get all scheduled transfers that should execute
        to_execute = []
        for schedule_id, transfer in self.scheduled_transfers.items():
            if transfer['execute_at'] <= timestamp:
                to_execute.append((schedule_id, transfer))
        
        # Sort by execute_at time (and schedule_id for stability)
        to_execute.sort(key=lambda x: (x[1]['execute_at'], x[0]))
        
        executed_count = 0
        for schedule_id, transfer in to_execute:
            # Try to execute the transfer
            result = self.transfer(
                transfer['from_id'],
                transfer['to_id'],
                transfer['amount'],
                transfer['execute_at']
            )
            
            # Remove from scheduled transfers regardless of success/failure
            if schedule_id in self.scheduled_transfers:
                del self.scheduled_transfers[schedule_id]
            
            # Count if successful
            if result is not None:
                executed_count += 1
        
        return executed_count
    
    def merge_accounts(self, a_id: str, b_id: str, merged_id: str, timestamp: int) -> int | None:
        """Merge two accounts into a new one.
        Returns the balance of merged_id on success; None on failure.
        """
        # Validate preconditions
        if a_id not in self.accounts or b_id not in self.accounts:
            return None
        if merged_id in self.accounts:
            return None
        if a_id == b_id or a_id == merged_id or b_id == merged_id:
            return None
        
        # Calculate combined balance
        combined_balance = self.accounts[a_id] + self.accounts[b_id]
        
        # Create merged account
        self.accounts[merged_id] = combined_balance
        
        # Mark source accounts as closed
        self.closed_accounts.add(a_id)
        self.closed_accounts.add(b_id)
        
        # Repoint any pending scheduled transfers
        for schedule_id, transfer in self.scheduled_transfers.items():
            if transfer['from_id'] == a_id or transfer['from_id'] == b_id:
                transfer['from_id'] = merged_id
            if transfer['to_id'] == a_id or transfer['to_id'] == b_id:
                transfer['to_id'] = merged_id
        
        # Append merge record to log
        self.transaction_log.append({
            'type': 'merge',
            'a_id': a_id,
            'b_id': b_id,
            'merged_id': merged_id,
            'timestamp': timestamp
        })
        
        return combined_balance
    
    def get_statement(self, account_id: str, start_ts: int, end_ts: int) -> int | None:
        """Count transactions where account_id participated in the given time range.
        Returns count; None only if account_id has no history and does not exist.
        """
        # Check if account exists or has existed
        if account_id not in self.accounts and account_id not in self.closed_accounts:
            # Check if account has any history in the log
            has_history = False
            for transaction in self.transaction_log:
                if transaction['type'] == 'deposit' and transaction.get('account_id') == account_id:
                    has_history = True
                    break
                elif transaction['type'] == 'transfer':
                    if transaction.get('from_id') == account_id or transaction.get('to_id') == account_id:
                        has_history = True
                        break
                elif transaction['type'] == 'merge':
                    if transaction.get('a_id') == account_id or transaction.get('b_id') == account_id or transaction.get('merged_id') == account_id:
                        has_history = True
                        break
            
            if not has_history:
                return None
        
        # Count transactions (only transfers and merges, not deposits)
        count = 0
        for transaction in self.transaction_log:
            ts = transaction.get('timestamp', 0)
            if start_ts <= ts <= end_ts:
                # Check if account participated (sender or receiver implies transfers only)
                if transaction['type'] == 'transfer':
                    if transaction.get('from_id') == account_id or transaction.get('to_id') == account_id:
                        count += 1
                elif transaction['type'] == 'merge':
                    # Merge record counts for the merged_id
                    if transaction.get('merged_id') == account_id:
                        count += 1
        
        return count