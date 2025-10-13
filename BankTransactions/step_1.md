You will be given an abstract Bank interface. Implement all methods described below in BankImpl.
General rules:

Amounts are integer cents (e.g., £12.34 → 1234).

Timestamps are integers (Unix-like seconds).

Account IDs and schedule IDs are non-empty strings.

Do not raise exceptions for invalid inputs—return the failure value specified for each method.

Later levels must not break earlier behavior.

Performance is not graded.


You must maintain internal balances and a transaction log [a list you design] for deposits/transfers.

create_account(self, account_id: str, initial_balance: int) -> bool
Create account with starting balance initial_balance.
Returns True if created; False if account_id already exists.

deposit(self, account_id: str, amount: int, timestamp: int) -> int | None
amount > 0. Increase balance; append a "deposit" record in your log.
Returns the new balance on success; None if account is unknown or amount <= 0.

transfer(self, from_id: str, to_id: str, amount: int, timestamp: int) -> int | None
amount > 0. Atomically move funds from from_id to to_id; append a "transfer" record.
Fails if either account is unknown or if from_id lacks funds at timestamp.
Returns the new balance of from_id on success; None on failure.

get_balance(self, account_id: str) -> int | None
Returns current balance; None if account unknown.