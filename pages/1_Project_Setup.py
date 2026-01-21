import streamlit as st
from firebase_manager import firebase_manager
import time

# --- HIDE DEFAULT NAVIGATION CSS INJECTION ---
st.markdown("""
<style>
/* Targets the automatically generated navigation div and hides it */
div[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)
# --------------------------------------------------

# Page configuration
st.set_page_config(
    page_title="Cognito-Spec",
    page_icon="logooo.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)
# --- CUSTOM SELECTION BOX NAVIGATION LOGIC ---
def navigate_with_selectbox():
    """Handles the sidebar selectbox navigation"""
    
    page_names = {
        "🏠 Home": "Home.py",
        "⚙️ Project Setup": "pages/1_Project_Setup.py",
        "💬 Interview": "pages/2_Interview.py",
        "🔍 Gap Analysis": "pages/3_Gap_Analysis.py",
        "📄 SRS Generation": "pages/4_Export.py"
    }
    
    # Determine current page name
    current_page_name = "⚙️ Project Setup"
    
    selected_page_name = st.selectbox(
        "**Go to Page:**", 
        options=list(page_names.keys()), 
        index=list(page_names.keys()).index(current_page_name),
        key="custom_sidebar_select"
    )
    
    # Check if the selected page is different from the current page and switch
    if selected_page_name != current_page_name:
        st.session_state.current_page = selected_page_name
        st.switch_page(page_names[selected_page_name])

# Initialize session state
def init_session_state():
    if 'project_initialized' not in st.session_state:
        st.session_state.project_initialized = False
    if 'project_id' not in st.session_state:
        st.session_state.project_id = None
    if 'project_name' not in st.session_state:
        st.session_state.project_name = ""
    if 'domain' not in st.session_state:
        st.session_state.domain = "Healthcare"
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'conflict_active' not in st.session_state:
        st.session_state.conflict_active = False
    if 'conflict_details' not in st.session_state:
        st.session_state.conflict_details = {}
    if 'requirements' not in st.session_state:
        st.session_state.requirements = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""

init_session_state()

# Sidebar navigation
with st.sidebar:
    
    try:
        st.image("logooo.png", width=270)
    except:
        st.title("🚀 Cognito-Spec") 
    st.markdown("---")

    # Custom Navigation Selectbox
    navigate_with_selectbox()

    st.markdown("---")
    
    # Project Info
    if st.session_state.project_initialized:
        st.subheader("Current Project Status")
        
        # Displaying all requested details
        status_icon = "✅ Initialized"
        req_count = len(st.session_state.requirements)
        
        st.markdown(f"**Name:** **`{st.session_state.project_name}`**")
        st.markdown(f"**Domain:** **`{st.session_state.domain}`**")
        st.markdown(f"**Status:** **`{status_icon}`**")
        st.markdown(f"**Requirements:** **`{req_count}`**")

st.title("⚙️ Project Setup")

# Project setup form
with st.form("project_setup"):
    st.subheader("Create New Project")
    
    project_name = st.text_input("Project Name", placeholder="Enter your project name...")
    domain = st.selectbox(
        "Domain",
        ["Healthcare",
            "Finance",
            "E-commerce",
            "Education",
            "Manufacturing",
            "Transportation / Logistics",
            "Media & Entertainment",
            "Telecommunications",
            "Other"]
    )
    
    submitted = st.form_submit_button("Initialize Project")
    
    if submitted:
        if not project_name:
            st.error("Please enter a project name")
        else:
            with st.spinner("Initializing your project..."):
                # Generate project ID
                project_id = f"project_{int(time.time())}"
                
                # Initialize session state
                st.session_state.project_initialized = True
                st.session_state.project_id = project_id
                st.session_state.project_name = project_name
                st.session_state.domain = domain
                st.session_state.chat_history = []
                st.session_state.conflict_active = False
                st.session_state.requirements = []
                
                # Initialize with welcome message
                from ai_controller import ai_controller
                welcome_question = ai_controller.elicit_requirement(domain)
                st.session_state.current_question = welcome_question
                
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": welcome_question
                })
                
                st.success("Project initialized successfully!")
                time.sleep(1)
                st.rerun()


# Navigation for initialized projects
if st.session_state.project_initialized:
    st.divider()
    st.subheader("Continue Working")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("Home.py")
    with col2:
        if st.button("💬 Interview", use_container_width=True):
            st.switch_page("pages/2_Interview.py")