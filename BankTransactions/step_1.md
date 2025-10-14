## Assigment

You will be given an abstract Bank interface. Implement all methods described below.
General rules:

Amounts are integer cents (e.g., £12.34 → 1234).

Timestamps are integers (Unix-like seconds).

Account IDs and schedule IDs are non-empty strings.

Do not raise exceptions for invalid inputs—return the failure value specified for each method.

Later levels must not break earlier behavior.

Performance is not graded.

## Step 1

You must maintain internal balances and a transaction log for deposits/transfers.

```python
create_account(self, account_id: str, initial_balance: int) -> bool
```
Create account with starting balance initial_balance.
Returns True if created; False if account_id already exists.

```python
deposit(self, account_id: str, amount: int) -> int | None
```
amount > 0. Increase balance; append a "deposit" record in your log.
Returns the new balance on success; None if account is unknown or amount <= 0.

```python
transfer(self, from_id: str, to_id: str, amount: int) -> int | None
```
amount > 0. Atomically move funds from from_id to to_id; append a "transfer" record.
Fails if either account is unknown or if from_id lacks funds.
Returns the new balance of from_id on success; None on failure.

```python
get_balance(self, account_id: str) -> int | None
```
Returns current balance; None if account unknown.