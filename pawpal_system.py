from dataclasses import dataclass, field
from enum import Enum


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

    def mark_complete(self):
        """Marks this task as completed."""
        self.completed = True

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

    def get_plan(self):
        """Returns today's plan for this owner."""
        return Scheduler().generate_plan(self)


class Scheduler:
    def __init__(self, date=None):
        self.date = date

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
