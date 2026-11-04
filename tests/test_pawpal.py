from pawpal_system import Pet, Task, Priority


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
