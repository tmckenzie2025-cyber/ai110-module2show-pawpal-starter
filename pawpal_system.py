from dataclasses import dataclass, field
from enum import Enum
from datetime import date, timedelta


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


PRIORITY_RANK = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}


@dataclass
class Pet:
    name: str
    type: str
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Adds a task to this pet's task list."""
        self.tasks.append(task)

    def get_info(self):
        """Returns the pet's name and type."""
        return f"{self.name} ({self.type})"


@dataclass
class Task:
    description: str
    duration_minutes: int
    priority: Priority
    pet: Pet
    frequency: str = "daily"
    completed: bool = False
    start_time: str = ''
    due_date: date = None

    def mark_complete(self):
        """Marks this task as completed. For daily or weekly tasks, also adds the next occurrence to the pet's tasks."""
        if self.completed:
            return
        self.completed = True
        if self.frequency == "daily":
            new_task = Task(self.description, self.duration_minutes,self.priority, self.pet, frequency = self.frequency , start_time = self.start_time , due_date = date.today()+ timedelta(days=1) )
            self.pet.add_task(new_task)
        elif self.frequency == "weekly":
            new_task = Task(self.description, self.duration_minutes,self.priority, self.pet, frequency = self.frequency , start_time = self.start_time , due_date = date.today() + timedelta(days=7) )
            self.pet.add_task(new_task)

    def remind(self):
        """Returns a reminder message for this task."""
        return (
            f"Reminder: {self.description} for {self.pet.name} "
            f"({self.duration_minutes} min, {self.priority.value} priority)"
        )


class Owner:
    def __init__(self, name, available_time):
        self.name = name
        self.available_time = available_time
        self.pets = []

    def add_pet(self, pet):
        """Adds a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Returns every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def filter_tasks(self, completed=None, pet_name=None):
        """Returns tasks filtered by completion status and/or pet name.

        completed: True/False to match status, None to ignore it.
        pet_name: case-insensitive pet name, None to ignore it.
        """
        tasks = self.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet.name.lower() == pet_name.lower()]
        return tasks

    def get_plan(self):
        """Returns today's plan for this owner."""
        return Scheduler().generate_plan(self)


class Scheduler:

    def sort_by_time(self, tasks):
        """Returns tasks sorted by start_time ("HH:MM"), earliest first.

        Zero-padded "HH:MM" strings compare correctly as plain strings,
        so the lambda can use the string itself as the sort key. Tasks
        with no start_time sort last.
        """
        return sorted(tasks, key=lambda t: (t.start_time == '', t.start_time))

    def generate_plan(self, owner):
        """Builds a plan of tasks that fit the owner's available time."""
        pending = [t for t in owner.get_all_tasks() if not t.completed]
        pending.sort(key=lambda t: (PRIORITY_RANK[t.priority], t.duration_minutes))

        plan = []
        remaining = owner.available_time
        for task in pending:
            if task.duration_minutes <= remaining:
                plan.append(task)
                remaining -= task.duration_minutes
        return plan

    def checker(self, tasks):
        """Returns a warning for each start time shared by two or more tasks.

        Returns an empty list when there are no conflicts.
        """
        by_time = {}
        for task in tasks:
            if task.start_time == '':
                continue
            by_time.setdefault(task.start_time, []).append(task)

        warnings = []
        for time, group in by_time.items():
            if len(group) > 1:
                names = ", ".join(f"{t.description} ({t.pet.name})" for t in group)
                warnings.append(f"Conflict at {time}: {names}")
        return warnings