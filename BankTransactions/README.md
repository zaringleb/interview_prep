# BankTransactions

Implement `bank.py` to pass four progressively harder test levels.

## Prerequisites
- Python 3.10+
- pytest

## Quickstart

```bash
# (optional) create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate

# install test runner
python -m pip install -U pip pytest

# verify the local test framework works
python -m pytest BankTransactions/test_framework.py -v
```

## Workflow

1. Read the current step spec in `step_1.md` (then `step_2.md`, etc.).
2. Update the `Bank` class in `bank.py`.
3. Run tests for the current level only (do not run previous levels yet).
4. Refactor as needed and proceed to the next level.

## Running tests

```bash
python -m pytest -q BankTransactions/test_level*.py
```

## Files
- `bank.py` — your implementation goes here
- `solution.py` — reference solution (check only after finishing)
- `step_*.md` — specifications for each level
- `test_level*.py` — tests for each level