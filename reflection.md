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
    One tradeoff my scheduler makes checker groups tasks by their exact start_time. If two or more tasks share a time, it returns a warning. It doesn’t compare durations, so a 30-minute task starting at 08:00 and a 10-minute task starting at 08:15 won’t be flagged.
- Why is that tradeoff reasonable for this scenario?
    Reasonable because its simple to read and test. Owners set each start time to a specific minute, so an exact match is a clear sign of a problem. The check only warns and never blocks the plan, so the owner can decide what to change.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
