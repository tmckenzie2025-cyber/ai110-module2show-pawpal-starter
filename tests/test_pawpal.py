from datetime import date, timedelta

from pawpal_system import Pet, Task, Priority, Scheduler, Owner


def test_mark_complete_changes_status():
    pet = Pet("Melo", "Cane Corso")
    task = Task("Walk", 30, Priority.HIGH, pet)
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Melo", "Cane Corso")
    task = Task("Walk", 30, Priority.HIGH, pet)
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    pet = Pet("Melo", "Cane Corso")
    late = Task("Dinner", 20, Priority.LOW, pet, start_time="18:30")
    early = Task("Walk", 30, Priority.HIGH, pet, start_time="07:00")
    mid = Task("Meds", 5, Priority.MEDIUM, pet, start_time="12:15")

    result = Scheduler().sort_by_time([late, early, mid])

    assert [t.description for t in result] == ["Walk", "Meds", "Dinner"]


def test_completing_daily_task_creates_task_for_next_day():
    pet = Pet("Melo", "Cane Corso")
    task = Task("Walk", 30, Priority.HIGH, pet, frequency="daily",
                start_time="08:00", due_date=date.today())
    pet.add_task(task)

    task.mark_complete()

    assert task.completed is True
    assert len(pet.tasks) == 2
    new_task = pet.tasks[1]
    assert new_task.due_date == date.today() + timedelta(days=1)
    assert new_task.completed is False
    assert new_task.description == "Walk"


def test_checker_flags_duplicate_start_times():
    owner = Owner("Moo", 120)
    melo, luna = Pet("Melo", "Dog"), Pet("Luna", "Cat")
    melo.add_task(Task("Walk", 30, Priority.HIGH, melo, start_time="09:00"))
    luna.add_task(Task("Feed", 10, Priority.HIGH, luna, start_time="09:00"))
    owner.add_pet(melo)
    owner.add_pet(luna)

    warnings = Scheduler().checker(owner.get_all_tasks())

    assert len(warnings) == 1
    assert "09:00" in warnings[0]
