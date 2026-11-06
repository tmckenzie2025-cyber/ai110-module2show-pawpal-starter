from datetime import datetime

import pandas as pd
import streamlit as st

from pawpal_system import Owner, Pet, Task, Priority, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planner that sorts your tasks, flags time conflicts, and builds a daily plan.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Moo", 120)

owner = st.session_state.owner
scheduler = Scheduler()


def normalize_time(text):
    """Returns 'HH:MM' (zero-padded) for valid input, '' for blank, None for invalid."""
    text = text.strip()
    if text == "":
        return ""
    try:
        return datetime.strptime(text, "%H:%M").strftime("%H:%M")
    except ValueError:
        return None


def friendly_time(hhmm):
    """'09:00' -> '9:00 AM'."""
    return datetime.strptime(hhmm, "%H:%M").strftime("%I:%M %p").lstrip("0")


def show_conflicts(conflicts):
    """Renders one plain-language warning per double-booked time slot."""
    if len(conflicts) > 1:
        st.warning(f"**{len(conflicts)} time slots are double-booked.** Details below.")
    for c in conflicts:
        names = [f"**{t.description}** ({t.pet.name})" for t in c.tasks]
        joined = " and ".join([", ".join(names[:-1]), names[-1]] if len(names) > 2 else names)
        if c.same_pet:
            pet_note = f"These are all for {c.tasks[0].pet.name}, who can't do them at the same time."
        else:
            pet_note = "You would need to do these at the same time."
        tip = (
            f"💡 Try moving **{c.tasks[-1].description}** to **{friendly_time(c.suggested_time)}**."
            if c.suggested_time
            else f"💡 Nothing is free later today for **{c.tasks[-1].description}**; try an earlier time."
        )
        st.warning(f"⚠️ **{friendly_time(c.start_time)} is double-booked**\n\n{joined} overlap. {pet_note}\n\n{tip}")


def task_table(tasks, conflicts=()):
    """Shows tasks in a table, highlighting rows that are part of a conflict."""
    flagged = {id(t) for c in conflicts for t in c.tasks}
    df = pd.DataFrame(task_rows(tasks))
    marks = [id(t) in flagged for t in tasks]
    styled = df.style.apply(
        lambda row: ["background-color: rgba(255, 193, 7, 0.25)" if marks[row.name] else "" for _ in row],
        axis=1,
    )
    st.dataframe(styled, hide_index=True, width="stretch")


def task_rows(tasks):
    """Converts tasks into table rows for st.table."""
    return [
        {
            "Time": t.start_time or "—",
            "Task": t.description,
            "Pet": t.pet.name,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority.value.capitalize(),
            "Repeats": t.frequency,
            "Status": "✅ Done" if t.completed else "⏳ Pending",
        }
        for t in tasks
    ]


# ---------- Owner & pets ----------
st.subheader("Owner & Pets")
owner.available_time = st.number_input(
    "Time available today (minutes)", min_value=0, max_value=1440, value=owner.available_time, step=5
)

col_a, col_b, col_c = st.columns([2, 1, 1])
with col_a:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_b:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col_c:
    st.write("")
    st.write("")
    add_pet = st.button("Add pet")

if add_pet:
    name = pet_name.strip()
    if not name:
        st.error("Please enter a pet name.")
    elif name.lower() in [p.name.lower() for p in owner.pets]:
        st.warning(f"{name} is already on your list.")
    else:
        owner.add_pet(Pet(name, species))
        st.success(f"Added {name} the {species}.")

if owner.pets:
    st.write("Your pets: " + ", ".join(p.get_info() for p in owner.pets))
else:
    st.info("Add a pet to get started.")

st.divider()

# ---------- Add a task ----------
st.subheader("Add a Task")

if owner.pets:
    with st.form("add_task_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            task_pet = st.selectbox("Pet", [p.name for p in owner.pets])
            task_title = st.text_input("Task title", value="Morning walk")
            start_time = st.text_input("Start time (HH:MM, optional)", value="08:00")
        with c2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
            priority = st.selectbox("Priority", ["high", "medium", "low"])
            frequency = st.selectbox("Repeats", ["daily", "weekly", "once"])
        submitted = st.form_submit_button("Add task")

    if submitted:
        time_value = normalize_time(start_time)
        if time_value is None:
            st.error("Start time must look like HH:MM, for example 08:30 or 17:45.")
        elif not task_title.strip():
            st.error("Please enter a task title.")
        else:
            pet = next(p for p in owner.pets if p.name == task_pet)
            pet.add_task(
                Task(
                    task_title.strip(),
                    int(duration),
                    Priority(priority),
                    pet,
                    frequency=frequency,
                    start_time=time_value,
                )
            )
            st.success(f"Added '{task_title.strip()}' for {pet.name}.")
else:
    st.caption("Add a pet above before creating tasks.")

st.divider()

# ---------- Schedule view: sorted, filtered, conflicts ----------
st.subheader("Task Schedule")

if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

all_tasks = owner.get_all_tasks()

if not all_tasks:
    st.info("No tasks yet. Add one above.")
else:
    f1, f2 = st.columns(2)
    with f1:
        pet_filter = st.selectbox("Show pet", ["All pets"] + [p.name for p in owner.pets])
    with f2:
        status_filter = st.selectbox("Show status", ["All", "Pending", "Completed"])

    completed_arg = {"All": None, "Pending": False, "Completed": True}[status_filter]
    pet_arg = None if pet_filter == "All pets" else pet_filter

    filtered = owner.filter_tasks(completed=completed_arg, pet_name=pet_arg)
    ordered = scheduler.sort_by_time(filtered)

    # Conflicts are only meaningful for tasks that still need doing.
    pending = owner.filter_tasks(completed=False)
    conflicts = scheduler.find_conflicts(pending)

    if conflicts:
        show_conflicts(conflicts)
    else:
        st.success("No scheduling conflicts among pending tasks.")

    if ordered:
        task_table(ordered, conflicts)
        if conflicts:
            st.caption("Highlighted rows are double-booked.")
    else:
        st.info("No tasks match those filters.")

    # ---------- Complete a task ----------
    if pending:
        st.markdown("#### Mark a task complete")
        pending_sorted = scheduler.sort_by_time(pending)
        choice = st.selectbox(
            "Task",
            range(len(pending_sorted)),
            format_func=lambda i: (
                f"{pending_sorted[i].start_time or 'no time'} · "
                f"{pending_sorted[i].description} ({pending_sorted[i].pet.name})"
            ),
        )
        if st.button("Mark complete"):
            task = pending_sorted[choice]
            before = len(task.pet.tasks)
            task.mark_complete()
            if len(task.pet.tasks) > before:
                st.session_state.flash = f"Completed '{task.description}'. Next {task.frequency} occurrence added."
            else:
                st.session_state.flash = f"Completed '{task.description}'."
            st.rerun()  # refresh the table above with the new status

st.divider()

# ---------- Daily plan ----------
st.subheader("Today's Plan")
st.caption("Picks pending tasks by priority (then shortest first) until your available time runs out.")

if st.button("Generate plan"):
    plan = owner.get_plan()
    pending_all = owner.filter_tasks(completed=False)
    skipped = [t for t in pending_all if t not in plan]

    if not plan:
        st.warning("Nothing fits in your available time. Add time or shorten some tasks.")
    else:
        used = sum(t.duration_minutes for t in plan)
        st.success(f"Planned {len(plan)} task(s) using {used} of {owner.available_time} minutes.")
        plan_conflicts = scheduler.find_conflicts(plan)
        task_table(scheduler.sort_by_time(plan), plan_conflicts)
        show_conflicts(plan_conflicts)

    if skipped:
        st.warning(
            "Not enough time for: "
            + ", ".join(f"{t.description} ({t.pet.name}, {t.duration_minutes} min)" for t in skipped)
        )
