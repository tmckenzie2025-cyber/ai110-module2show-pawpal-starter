# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
- Track a pet
- Track task
- Generate a daily plan

- Briefly describe your initial UML design.
    -
- What classes did you include, and what responsibilities did you assign to each?
    -Pet: Holds its name and type and returns them when asked.
    -Task: Holds one care job’s type, time, and priority, and reminds the owner when it’s due.
    -Owner: Keeps track of the owner’s pets and tasks, and asks for the day’s plan.
    -Scheduler: Builds the day’s plan from the tasks and the time block.
**b. Design changes**

- Did your design change during implementation?
    -Yes
- If yes, describe at least one change and why you made it.
    -Task didn’t know which pet it belonged to. Now it does.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    Total available time: Owner is created with 120 minutes.
    Priority: high, medium, and low, in that order.
    Duration: shorter tasks are preferred within the same priority.
    Completion: completed tasks are left out of today’s plan.
- How did you decide which constraints mattered most?


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    One tradeoff my scheduler makes: `main.py` uses `Scheduler.checker()`, which groups tasks by their exact start_time. If two or more tasks share a time, it returns a warning. It doesn’t compare durations, so a 30-minute task starting at 08:00 and a 10-minute task starting at 08:15 won’t be flagged by `main.py`. The Streamlit app avoids this by using `Scheduler.find_conflicts()`, which is duration-aware and catches overlaps, but I kept the simpler `checker()` in `main.py`.
- Why is that tradeoff reasonable for this scenario?
    Reasonable because its simple to read and test. Owners set each start time to a specific minute, so an exact match is a clear sign of a problem. The check only warns and never blocks the plan, so the owner can decide what to change.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    Brainstorming small improvements to the scheduler, with pawpal_system.py and main.py attached.
    Getting help with a sorted() lambda key for “HH:MM” times, and filtering methods.
    Reviewing a refactoring suggestion for mark_complete and deciding which version to keep.
- What kinds of prompts or questions were most helpful?
    Asking for one change at a time, with a limit, such as “change only this method and nothing else.”
    Asking the AI to explain why something works, such as how the lambda key sorts. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    The base date. The AI suggested using self.due_date as the base for the next due date. You kept date.today(), because your Step 3 hint said “today + 1 day."
- How did you evaluate or verify what the AI suggested?
    Running the code. You ran main.py after each change, and the traceback showed the None problem with due_date.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested three behaviors: sorting tasks by start time, creating the next task when a daily task is completed, and flagging tasks that share a start time. I also kept two basic tests (marking a task complete, and adding a task to a pet).

- Why were these tests important?
    These matter because they are the core of the scheduler. If sorting, recurrence, or conflict detection is wrong, the plan the owner sees is wrong.

**b. Confidence** 

- How confident are you that your scheduler works correctly?
    I'm moderately confident, about 3 out of 5. The main paths work and all 5 tests pass, but I only tested the normal cases.
- What edge cases would you test next if you had more time?
    With more time I'd test:
    Overlapping tasks, such as a 60-minute task at 9:00 and another at 9:30 (this is what `find_conflicts()` handles, but it has no test yet).
    Non-padded times like "9:00", which sort after "10:00" as strings.
    Completed tasks being counted in conflict checks.
    Future-dated recurring copies showing up in today's plan.
    Zero available time and tasks longer than the time available.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I'm most satisfied with building the logic in small, tested pieces. Sorting, recurrence, and conflict warnings each worked on their own before I connected them, which made problems easier to find.
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    main.py still uses the exact-match `checker()`, while the Streamlit app uses the duration-aware `find_conflicts()`. I'd switch main.py to `find_conflicts()` (or pass it only pending tasks) so completed tasks and tomorrow's recurring copies stop counting as conflicts, since they share a start time with the original. Ignoring task duration in `checker()` was a documented tradeoff, not a bug I missed. I'd also add an edit button so a task can be moved without re-adding it.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    AI works best when I ask for one small change at a time and then check it by running the code.