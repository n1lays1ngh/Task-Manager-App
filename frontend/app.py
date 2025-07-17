import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Task Manager", layout="wide")
st.title("📝 Task Manager App")

# Create 2 columns: Add task (left), Task list (right)
left_col, right_col = st.columns([1, 2])  # Wider right column for tasks

# --- LEFT: Add New Task ---
with left_col:
    st.subheader("➕ Add New Task")
    with st.form("task_form", clear_on_submit=True):
        title = st.text_input("Title")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Add Task")

        if submitted:
            if title.strip() == "":
                st.warning("⚠️ Task title cannot be empty.")
            else:
                new_task = {
                    "title": title,
                    "description": description,
                    "completed": False
                }
                res = requests.post(f"{API_URL}/tasks", json=new_task)
                if res.status_code == 200:
                    st.success("✅ Task added!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add task.")
                    st.json(res.json())

# --- RIGHT: Show Tasks ---
with right_col:
    st.subheader("📋 Your Tasks")

    response = requests.get(f"{API_URL}/tasks")
    if response.status_code == 200:
        tasks = response.json()

        if not tasks:
            st.info("No tasks available.")
        else:
            tasks.sort(key=lambda t: t["completed"])  
            for task in tasks:
                
                left_col, complete_col, delete_col = st.columns([6, 2, 1])
                with left_col:
                    st.markdown(f"**{task['title']}**")
                    st.markdown(f"<span style='font-size: 13px;'>{task['description']}</span>", unsafe_allow_html=True)

                    if task["completed"]:
                        st.markdown("<span style='color: green;'>✅ Task Completed</span>", unsafe_allow_html=True)

                if not task["completed"]:
                    with complete_col:
                        if st.button("✅ Complete", key=f"complete{task['id']}"):
                            update_data = {
                                "title": task["title"],
                                "description": task["description"],
                                "completed": True
                            }
                            res = requests.put(f"{API_URL}/tasks/{task['id']}", json=update_data)
                            if res.status_code == 200:
                                st.success("🎉 Task marked as completed!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update task.")

                with delete_col:
                    if st.button("🗑️", key=f"del{task['id']}"):
                        res = requests.delete(f"{API_URL}/tasks/{task['id']}")
                        if res.status_code == 200:
                            st.success("🗑️ Task deleted")
                            st.rerun()
                        else:
                            st.error("❌ Could not delete task")
    else:

        st.error("⚠️ Couldn't fetch tasks from the backend.")

        





