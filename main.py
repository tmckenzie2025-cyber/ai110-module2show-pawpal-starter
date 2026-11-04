from pawpal_system import Owner, Pet, Task, Priority

owner = Owner("Moo", 120)
melo = Pet("Melo", "Cane Corso")
woody = Pet("Woody", "Bulldog")
owner.add_pet(melo)
owner.add_pet(woody)

walk = Task("Walk", 30, Priority.HIGH, melo)
feeding = Task("Feeding", 10, Priority.HIGH, woody)
grooming = Task("Grooming", 45, Priority.LOW, melo)
melo.add_task(walk)
woody.add_task(feeding)
melo.add_task(grooming)

print("Today's Schedule")
for task in owner.get_plan():
    print(task.remind())
