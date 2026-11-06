from pawpal_system import Owner, Pet, Task, Priority, Scheduler

owner = Owner("Moo", 120)
melo = Pet("Melo", "Cane Corso")
woody = Pet("Woody", "Bulldog")
owner.add_pet(melo)
owner.add_pet(woody)

# Tasks added deliberately out of chronological order
grooming = Task("Grooming", 45, Priority.LOW, melo, start_time="14:00")
walk = Task("Walk", 30, Priority.HIGH, melo, start_time="08:00")
playtime = Task("Playtime", 20, Priority.MEDIUM, woody, start_time="17:30")
feeding = Task("Feeding", 10, Priority.HIGH, woody, start_time="06:00")
meds = Task("Medication", 5, Priority.HIGH, woody, start_time="09:15")
brushing = Task("Brushing", 15, Priority.LOW, woody, start_time="17:30")
woody.add_task(brushing)
melo.add_task(grooming)
woody.add_task(playtime)
melo.add_task(walk)
woody.add_task(feeding)
woody.add_task(meds)

# Mark a couple complete so the status filter has something to show
feeding.mark_complete()
walk.mark_complete()

scheduler = Scheduler()


def show(title, tasks):
    print(f"\n{title}")
    if not tasks:
        print("  (none)")
    for t in tasks:
        status = "done" if t.completed else "todo"
        print(f"  {t.start_time}  {t.description:<11} {t.pet.name:<6} [{status}]")


show("All tasks (as added, out of order)", owner.get_all_tasks())
show("Sorted by time", scheduler.sort_by_time(owner.get_all_tasks()))
show("Pending only", owner.filter_tasks(completed=False))
show("Completed only", owner.filter_tasks(completed=True))
show("Melo's tasks", owner.filter_tasks(pet_name="Melo"))
show(
    "Woody's pending tasks, sorted by time",
    scheduler.sort_by_time(owner.filter_tasks(completed=False, pet_name="Woody")),
)

print("\nToday's Schedule")
for task in scheduler.sort_by_time(owner.get_plan()):
    print(task.remind())

print("\nConflict check")
for warning in scheduler.checker(owner.get_all_tasks()):
    print(warning)