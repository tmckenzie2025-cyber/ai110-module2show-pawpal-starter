# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

Run the tests from the project root:

```bash
python -m pytest
```

The tests in `tests/test_pawpal.py` cover:

- **Task basics:** marking a task complete updates its status, and adding a task to a pet increases the pet's task count.
- **Sorting correctness:** `Scheduler.sort_by_time` returns tasks in chronological order.
- **Recurrence logic:** completing a daily task creates a new, incomplete task due the following day.
- **Conflict detection:** `Scheduler.checker` flags tasks that share the same start time, including across different pets.

Successful test run:

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/moo/Documents/VS Code/Python Pratice/Code_Path/PawPal/ai110-module2show-pawpal-starter
plugins: anyio-4.10.0
collected 5 items

tests/test_pawpal.py .....                                               [100%]

============================== 5 passed in 0.01s ===============================
```
Confidence Level 

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time() | Orders tasks by their "HH:MM" start time, earliest first; tasks with no start time go last. |
| Filtering | Owner.filter_tasks() | Returns tasks across all pets, narrowed by completion status and/or pet name (case-insensitive). |
| Conflict handling | Scheduler.checker() | Flags every start time shared by two or more tasks and returns a warning for each; returns an empty list if none. |
| Recurring tasks | Task.mark_complete() | Completing a daily or weekly task automatically adds the next occurrence to the pet, due 1 or 7 days out. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
