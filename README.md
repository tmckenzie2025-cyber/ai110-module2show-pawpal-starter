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

## ✨ Features

- Sorting by time: `Scheduler.sort_by_time()` orders tasks by their `HH:MM` start time, earliest first. Tasks with no start time go last, and tasks with equal times keep the order they were added.
- Filtering: `Owner.filter_tasks()` narrows tasks across all pets by completion status and/or pet name (case-insensitive).
- Conflict warnings:
  - `Scheduler.checker()` flags every start time shared by two or more tasks and returns one warning per time (used by `main.py`).
  - `Scheduler.find_conflicts()` is duration-aware. It flags tasks whose time windows overlap, treats back-to-back tasks as fine, and suggests the next free slot for the last task. It also records whether the clash is for one pet or across pets (used by the Streamlit app).
- Daily and weekly recurrence: completing a daily or weekly task with `Task.mark_complete()` automatically adds the next occurrence to the pet, due 1 or 7 days out. Completing a task twice does not duplicate it, and `"once"` tasks do not repeat.
- Priority-based daily plan: `Scheduler.generate_plan()` takes pending tasks in order of priority (high, medium, low), shortest first within a priority, and adds each one that still fits in the owner's available time. Tasks that don't fit are skipped and reported in the app.
- Input validation (Streamlit): start times must be valid `HH:MM` (`9:00` is normalized to `09:00`), duplicate pet names are rejected, and empty titles are refused.

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

### Test coverage

The suite has 5 tests covering:
- Marking a task complete
- Adding a task to a pet
- Sorting tasks by start time
- Creating the next daily task when a daily task is completed
- Flagging tasks that share a start time

Not yet covered: weekly recurrence, `Owner.filter_tasks`, and the overlap check in `Scheduler.find_conflicts`.

Confidence Level ⭐⭐⭐

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time() | Orders tasks by their "HH:MM" start time, earliest first; tasks with no start time go last. |
| Filtering | Owner.filter_tasks() | Returns tasks across all pets, narrowed by completion status and/or pet name (case-insensitive). |
| Conflict handling | Scheduler.checker() | Flags every start time shared by two or more tasks and returns a warning for each; returns an empty list if none. |
| Recurring tasks | Task.mark_complete() | Completing a daily or weekly task automatically adds the next occurrence to the pet, due 1 or 7 days out. |

## 📸 Demo Walkthrough

### Main UI features

The Streamlit app (`python -m streamlit run app.py`) lets you:

- Set your available time for the day and add pets (name and species).
- Add tasks for a chosen pet: title, duration, priority, repeat frequency (daily, weekly, once), and an optional start time.
- View the task schedule in a table sorted by start time, filtered by pet and by status (All, Pending, Completed).
- See conflict warnings above the table, with the affected rows highlighted.
- Mark a task complete, which adds the next occurrence for daily and weekly tasks.
- Generate today's plan, which shows the tasks that fit your available time and lists any that didn't.

### Example workflow

1. Add a pet. Enter "Mochi", choose "dog", and click *Add pet*.
2. Schedule a task. Add "Walk" at `09:00` (30 min, high priority, daily).
3. Add a second task "Feed" at `9:00`. The app normalizes the time to `09:00` and shows a warning: *9:00 AM is double-booked*, naming both tasks and suggesting a new time for "Feed". Both rows are highlighted.
4. Resolve the clash. The app has no edit button, so either mark the clashing task complete or add it again at the suggested time. Completed tasks no longer count toward conflicts.
5. View the schedule. The table is sorted by time, and the filters narrow it to one pet or to pending tasks.
6. Mark "Walk" complete. A success message confirms that tomorrow's walk was added automatically.
7. Click *Generate plan*. The app shows the tasks that fit your available time in time order, with a summary such as "Planned 2 task(s) using 40 of 120 minutes."

### Key scheduler behaviors shown

- Sorting: tasks added out of order appear chronologically, with untimed tasks last.
- Filtering: by pet and by completion status.
- Conflict warnings: plain-language warnings with a suggested free slot.
- Recurrence: completing a daily or weekly task creates the next occurrence.
- Plan building: high-priority and short tasks are placed first, and anything that doesn't fit is reported.

### Sample CLI output

`python main.py` adds tasks out of order, completes two of them, and prints the sorted, filtered, and conflict views:

```
All tasks (as added, out of order)
  14:00  Grooming    Melo   [todo]
  08:00  Walk        Melo   [done]
  08:00  Walk        Melo   [todo]
  17:30  Brushing    Woody  [todo]
  17:30  Playtime    Woody  [todo]
  06:00  Feeding     Woody  [done]
  09:15  Medication  Woody  [todo]
  06:00  Feeding     Woody  [todo]

Sorted by time
  06:00  Feeding     Woody  [done]
  06:00  Feeding     Woody  [todo]
  08:00  Walk        Melo   [done]
  08:00  Walk        Melo   [todo]
  09:15  Medication  Woody  [todo]
  14:00  Grooming    Melo   [todo]
  17:30  Brushing    Woody  [todo]
  17:30  Playtime    Woody  [todo]

Pending only
  14:00  Grooming    Melo   [todo]
  08:00  Walk        Melo   [todo]
  17:30  Brushing    Woody  [todo]
  17:30  Playtime    Woody  [todo]
  09:15  Medication  Woody  [todo]
  06:00  Feeding     Woody  [todo]

Completed only
  08:00  Walk        Melo   [done]
  06:00  Feeding     Woody  [done]

Melo's tasks
  14:00  Grooming    Melo   [todo]
  08:00  Walk        Melo   [done]
  08:00  Walk        Melo   [todo]

Woody's pending tasks, sorted by time
  06:00  Feeding     Woody  [todo]
  09:15  Medication  Woody  [todo]
  17:30  Brushing    Woody  [todo]
  17:30  Playtime    Woody  [todo]

Today's Schedule
Reminder: Feeding for Woody (10 min, high priority)
Reminder: Walk for Melo (30 min, high priority)
Reminder: Medication for Woody (5 min, high priority)
Reminder: Playtime for Woody (20 min, medium priority)
Reminder: Brushing for Woody (15 min, low priority)

Conflict check
Conflict at 08:00: Walk (Melo), Walk (Melo)
Conflict at 17:30: Brushing (Woody), Playtime (Woody)
Conflict at 06:00: Feeding (Woody), Feeding (Woody)
```

Notes on this output:

- The completed "Feeding" and "Walk" each appear twice. Completing a daily task adds tomorrow's copy with the same start time, which is why each shows once as `[done]` and once as `[todo]`.
- Because `main.py` uses `Scheduler.checker()`, which compares start times only, those completed/recurring pairs are reported as "conflicts" (for example, `Walk (Melo), Walk (Melo)`). The real conflict is `Brushing` and `Playtime` at 17:30. The Streamlit app avoids this by checking only pending tasks.
- Today's plan lists tasks by priority, then by shortest duration, until the available time runs out. `Grooming` (45 min, low priority) is left out because it no longer fits.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
