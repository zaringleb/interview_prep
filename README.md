## Goal

We are building a practice assignment that closely mimics Industry Coding Framework (ICF) interviews — a 90-minute, multi-stage code exercise.
The idea is to reproduce the real experience, not just the algorithmic challenge: the candidate must design, evolve, and repeatedly refactor a working system as requirements expand.

## How this interview differs from typical LeetCode-style problems

| Aspect | ICF | LeetCode-style |
| --- | --- | --- |
| Nature of task | One long project with 3–4 “levels”; each adds new requirements to the same codebase. | One isolated algorithmic puzzle per question. |
| Goal | Build and evolve a small software system that behaves correctly through changing specs. | Produce an optimal algorithm for a fixed spec. |
| Evaluation | Counts passed tests; partial credit for every passing case; correctness and adaptability matter more than speed. | All-or-nothing per test; runtime and memory complexity critical. |
| Skills tested | Reading ambiguous specs, incremental design, code hygiene, extensibility, and quick debugging. | Pattern recognition and theoretical algorithm design. |
| Pressure points | Requirements evolve mid-problem → forces refactor. Candidate must balance rewriting vs hacking. | Single implementation; rarely modified. |

## What makes a good ICF-style task

- Incremental structure — Each level adds realistic features (e.g., “add metrics”, “add scheduling”, “merge entities”).
- Hidden dependency between levels — A naive early design (e.g., only storing current balances) will break later (when time, history, or merges appear). This intentionally pressures the candidate to rethink architecture.
- Conceptual simplicity, implementation depth — Operations use ordinary logic (no advanced algorithms) but require clean handling of state, data integrity, and evolving requirements.
- Tolerant grading — Partial credit per successful test; resubmissions allowed; correctness is more important than elegance.
- Refactor stimulus — Level 3–4 introduce features (time travel, idempotency, merges, immutability) that invalidate early shortcuts, ensuring the candidate must re-architect rather than append ad-hoc code.
- Natural domain — Problems feel like small real systems: banking, file storage, task schedulers, or versioned data stores.