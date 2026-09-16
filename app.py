import streamlit as st
import time
from datetime import date
import database

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Study Planner",
    page_icon="📚",
    layout="wide"
)

database.create_tables()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
}

.subtitle {
    font-size: 18px;
    color: #777;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📚 Study Planner")

st.sidebar.caption(
    "Organize your study. Stay consistent."
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📝 Tasks",
        "📅 Weekly Plan",
        "📚 Subjects",
        "🍅 Pomodoro",
        "📖 Notes"
    ]
)

st.sidebar.divider()

st.sidebar.write("🎓 Engineering Student")
st.sidebar.write("💻 Python • C")


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">📚 Study Planner</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Plan your study. Track your progress. 🚀'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    tasks = database.get_tasks()
    subjects = database.get_subjects()

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks if task[4] == 1
    )

    pending_tasks = total_tasks - completed_tasks

    progress = (
        completed_tasks / total_tasks
        if total_tasks > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📚 Subjects",
            len(subjects)
        )

    with col2:
        st.metric(
            "📝 Total Tasks",
            total_tasks
        )

    with col3:
        st.metric(
            "⏳ Pending",
            pending_tasks
        )

    with col4:
        st.metric(
            "✅ Completed",
            completed_tasks
        )

    st.divider()

    st.subheader("📈 Overall Progress")

    st.progress(progress)

    st.write(
        f"**{completed_tasks} / {total_tasks} tasks completed**"
    )

    st.divider()

    st.subheader("📅 Today")

    st.info(
        date.today().strftime("%A, %d %B %Y")
    )

    st.subheader("🎯 Motivation")

    quotes = [
        "Small progress every day becomes big results. 💪",
        "Consistency is more important than perfection. 🔥",
        "Learn today. Build tomorrow. 🚀",
        "Keep going. You're improving every day. 💻"
    ]

    st.success(
        quotes[date.today().day % len(quotes)]
    )


# =========================================================
# TASKS
# =========================================================

elif page == "📝 Tasks":

    st.header("📝 My Tasks")

    subjects = database.get_subjects()

    with st.form("add_task_form"):

        title = st.text_input(
            "Task name",
            placeholder="Example: Practice Python loops"
        )

        subject = st.selectbox(
            "Subject",
            subjects
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"]
        )

        add_task = st.form_submit_button(
            "➕ Add Task"
        )

        if add_task:

            if title.strip():

                database.add_task(
                    title.strip(),
                    subject,
                    priority
                )

                st.success(
                    "Task added successfully! 🎉"
                )

                time.sleep(0.5)
                st.rerun()

            else:

                st.warning(
                    "Please enter a task name."
                )

    st.divider()

    st.subheader("📋 Your Tasks")

    tasks = database.get_tasks()

    if not tasks:

        st.info(
            "No tasks yet. Add your first task above."
        )

    else:

        for task in tasks:

            task_id = task[0]
            title = task[1]
            subject = task[2]
            priority = task[3]
            completed = task[4]

            col1, col2, col3, col4 = st.columns(
                [0.6, 4, 2, 1]
            )

            with col1:

                checked = st.checkbox(
                    "",
                    value=bool(completed),
                    key=f"complete_{task_id}"
                )

                if checked != bool(completed):

                    database.update_task(
                        task_id,
                        checked
                    )

                    st.rerun()

            with col2:

                if completed:

                    st.markdown(
                        f"~~{title}~~"
                    )

                else:

                    st.write(
                        f"**{title}**"
                    )

            with col3:

                st.write(
                    f"📚 {subject}"
                )

                st.caption(
                    f"Priority: {priority}"
                )

            with col4:

                if st.button(
                    "🗑️",
                    key=f"delete_{task_id}"
                ):

                    database.delete_task(
                        task_id
                    )

                    st.rerun()


# =========================================================
# WEEKLY PLAN
# =========================================================

elif page == "📅 Weekly Plan":

    st.header("📅 Weekly Study Plan")

    st.write(
        "Create and save a study plan for each day."
    )

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    for day in days:

        current_plan = database.get_weekly_plan(day)

        with st.expander(
            f"📌 {day}"
        ):

            plan = st.text_area(
                f"Study plan for {day}",
                value=current_plan,
                key=f"plan_{day}",
                placeholder=(
                    "Example: Python - Functions "
                    "and practice"
                )
            )

            if st.button(
                f"💾 Save {day}",
                key=f"save_{day}"
            ):

                database.save_weekly_plan(
                    day,
                    plan
                )

                st.success(
                    f"{day} plan saved!"
                )


# =========================================================
# SUBJECTS
# =========================================================

elif page == "📚 Subjects":

    st.header("📚 Subjects")

    st.write(
        "Manage the subjects you are studying."
    )

    with st.form("subject_form"):

        new_subject = st.text_input(
            "Subject name",
            placeholder="Example: Mathematics"
        )

        add_subject = st.form_submit_button(
            "➕ Add Subject"
        )

        if add_subject:

            if new_subject.strip():

                database.add_subject(
                    new_subject.strip()
                )

                st.success(
                    f"{new_subject} added!"
                )

                time.sleep(0.5)
                st.rerun()

            else:

                st.warning(
                    "Please enter a subject."
                )

    st.divider()

    st.subheader("📖 Your Subjects")

    subjects = database.get_subjects()

    for subject in subjects:

        st.write(
            f"📘 **{subject}**"
        )


# =========================================================
# POMODORO
# =========================================================

elif page == "🍅 Pomodoro":

    st.header("🍅 Pomodoro Timer")

    st.write(
        "Focus on your study for a fixed amount of time."
    )

    study_minutes = st.number_input(
        "Study duration (minutes)",
        min_value=1,
        max_value=120,
        value=25
    )

    st.divider()

    st.subheader(
        f"⏱️ {study_minutes} minute study session"
    )

    if st.button(
        "▶️ Start Study Session",
        use_container_width=True
    ):

        total_seconds = study_minutes * 60

        progress_bar = st.progress(0)

        timer_text = st.empty()

        for remaining in range(
            total_seconds,
            0,
            -1
        ):

            minutes = remaining // 60
            seconds = remaining % 60

            timer_text.markdown(
                f"# ⏳ {minutes:02d}:{seconds:02d}"
            )

            progress = (
                total_seconds - remaining
            ) / total_seconds

            progress_bar.progress(progress)

            time.sleep(1)

        timer_text.markdown(
            "# 🎉 Study session complete!"
        )

        progress_bar.progress(1)

        st.balloons()


# =========================================================
# NOTES
# =========================================================

elif page == "📖 Notes":

    st.header("📖 Study Notes")

    saved_notes = database.get_notes()

    notes = st.text_area(
        "Write your notes",
        value=saved_notes,
        height=450,
        placeholder=(
            "Write your Python, C, Mathematics "
            "or other study notes here..."
        )
    )

    if st.button(
        "💾 Save Notes",
        use_container_width=True
    ):

        database.save_notes(notes)

        st.success(
            "Notes saved successfully! ✅"
        )

    st.divider()

    st.subheader("👀 Saved Notes")

    if saved_notes:

        st.markdown(saved_notes)

    else:

        st.info(
            "Your saved notes will appear here."
        )
