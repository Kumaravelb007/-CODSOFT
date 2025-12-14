import streamlit as st
from datetime import datetime
import json

# Page configuration
st.set_page_config(page_title="To-Do List Manager", page_icon="✅", layout="wide")

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'task_id_counter' not in st.session_state:
    st.session_state.task_id_counter = 1

# Helper functions
def add_task(title, description, priority, due_date):
    task = {
        'id': st.session_state.task_id_counter,
        'title': title,
        'description': description,
        'priority': priority,
        'due_date': due_date.strftime('%Y-%m-%d') if due_date else None,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    st.session_state.tasks.append(task)
    st.session_state.task_id_counter += 1
    return True

def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task_id]

def toggle_task(task_id):
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break

def update_task(task_id, title, description, priority, due_date):
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['title'] = title
            task['description'] = description
            task['priority'] = priority
            task['due_date'] = due_date.strftime('%Y-%m-%d') if due_date else None
            break

def get_priority_color(priority):
    colors = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
    return colors.get(priority, '⚪')

# Main UI
st.title("✅ To-Do List Manager")
st.markdown("---")

# Sidebar for adding new tasks
with st.sidebar:
    st.header("➕ Add New Task")
    
    with st.form("add_task_form", clear_on_submit=True):
        new_title = st.text_input("Task Title*", placeholder="Enter task title")
        new_description = st.text_area("Description", placeholder="Enter task description")
        new_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        new_due_date = st.date_input("Due Date", value=None)
        
        submit_button = st.form_submit_button("Add Task", use_container_width=True)
        
        if submit_button:
            if new_title.strip():
                add_task(new_title, new_description, new_priority, new_due_date)
                st.success("✅ Task added successfully!")
                st.rerun()
            else:
                st.error("⚠️ Task title is required!")
    
    st.markdown("---")
    
    # Statistics
    st.header("📊 Statistics")
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len([t for t in st.session_state.tasks if t['completed']])
    pending_tasks = total_tasks - completed_tasks
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", total_tasks)
        st.metric("Completed", completed_tasks)
    with col2:
        st.metric("Pending", pending_tasks)
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            st.metric("Progress", f"{completion_rate:.0f}%")

# Main content area
tab1, tab2 = st.tabs(["📋 All Tasks", "✏️ Manage Tasks"])

with tab1:
    # Filter options
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
    
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Created", "Priority", "Due Date"])
    
    # Filter tasks
    filtered_tasks = st.session_state.tasks.copy()
    
    if filter_status == "Pending":
        filtered_tasks = [t for t in filtered_tasks if not t['completed']]
    elif filter_status == "Completed":
        filtered_tasks = [t for t in filtered_tasks if t['completed']]
    
    if filter_priority != "All":
        filtered_tasks = [t for t in filtered_tasks if t['priority'] == filter_priority]
    
    # Sort tasks
    if sort_by == "Priority":
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        filtered_tasks.sort(key=lambda x: priority_order[x['priority']])
    elif sort_by == "Due Date":
        filtered_tasks.sort(key=lambda x: x['due_date'] if x['due_date'] else '9999-99-99')
    
    st.markdown("---")
    
    if not filtered_tasks:
        st.info("📝 No tasks found. Add your first task using the sidebar!")
    else:
        for task in filtered_tasks:
            with st.container():
                col1, col2, col3 = st.columns([0.5, 8, 1.5])
                
                with col1:
                    checked = st.checkbox("", value=task['completed'], key=f"check_{task['id']}", 
                                        label_visibility="collapsed")
                    if checked != task['completed']:
                        toggle_task(task['id'])
                        st.rerun()
                
                with col2:
                    title_style = "text-decoration: line-through; opacity: 0.6;" if task['completed'] else ""
                    st.markdown(f"<h4 style='{title_style}'>{get_priority_color(task['priority'])} {task['title']}</h4>", 
                              unsafe_allow_html=True)
                    
                    if task['description']:
                        st.markdown(f"*{task['description']}*")
                    
                    info_parts = []
                    if task['due_date']:
                        info_parts.append(f"📅 Due: {task['due_date']}")
                    info_parts.append(f"⏰ Created: {task['created_at']}")
                    st.caption(" | ".join(info_parts))
                
                with col3:
                    if st.button("🗑️ Delete", key=f"del_{task['id']}", use_container_width=True):
                        delete_task(task['id'])
                        st.rerun()
                
                st.markdown("---")

with tab2:
    st.header("✏️ Edit Tasks")
    
    if not st.session_state.tasks:
        st.info("📝 No tasks available to edit.")
    else:
        task_titles = [f"{t['id']}: {t['title']}" for t in st.session_state.tasks]
        selected_task_str = st.selectbox("Select a task to edit", task_titles)
        
        if selected_task_str:
            selected_id = int(selected_task_str.split(":")[0])
            selected_task = next((t for t in st.session_state.tasks if t['id'] == selected_id), None)
            
            if selected_task:
                st.markdown("---")
                
                with st.form("edit_task_form"):
                    edit_title = st.text_input("Task Title*", value=selected_task['title'])
                    edit_description = st.text_area("Description", value=selected_task['description'])
                    edit_priority = st.selectbox("Priority", ["Low", "Medium", "High"], 
                                                index=["Low", "Medium", "High"].index(selected_task['priority']))
                    
                    edit_due_date = None
                    if selected_task['due_date']:
                        edit_due_date = st.date_input("Due Date", 
                                                     value=datetime.strptime(selected_task['due_date'], '%Y-%m-%d'))
                    else:
                        edit_due_date = st.date_input("Due Date", value=None)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_button = st.form_submit_button("💾 Update Task", use_container_width=True)
                    with col2:
                        cancel_button = st.form_submit_button("❌ Cancel", use_container_width=True)
                    
                    if update_button:
                        if edit_title.strip():
                            update_task(selected_id, edit_title, edit_description, edit_priority, edit_due_date)
                            st.success("✅ Task updated successfully!")
                            st.rerun()
                        else:
                            st.error("⚠️ Task title is required!")

#Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Developed with ❤️ using Streamlit</div>", unsafe_allow_html=True)
