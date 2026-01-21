import streamlit as st
from ai_controller import ai_controller
from firebase_manager import firebase_manager

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
    current_page_name = "💬 Interview"
    
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

st.title("💬 Requirements Interview")

if not st.session_state.project_initialized:
    st.warning("Please initialize your project first.")
    st.switch_page("pages/1_Project_Setup.py")

# Layout: 70% Chat, 30% Dashboard
col_chat, col_dashboard = st.columns([2, 1])

with col_dashboard:
    st.subheader("📋 Requirements Dashboard")
    
    # Refresh requirements from Firestore
    if st.session_state.project_id:
        requirements = firebase_manager.fetch_all_requirements(st.session_state.project_id)
        st.session_state.requirements = requirements
    
    if st.session_state.requirements:
        # Group requirements by classification
        req_by_type = {}
        for req in st.session_state.requirements:
            req_type = req.get('classification', 'Unknown')
            if req_type not in req_by_type:
                req_by_type[req_type] = []
            req_by_type[req_type].append(req)
        
        # Display requirements by type with expanders
        type_labels = {
            "FR": "🚀 Functional Requirements",
            "NFR": "⚡ Non-Functional Requirements", 
            "IR": "🚫 Inverse Requirements",
            "DR": "🏢 Domain Requirements",
            "Constraint": "🔧 Constraints",
            "Unknown": "❓ Other Requirements"
        }
        
        for req_type in ["FR", "NFR", "IR", "DR", "Constraint", "Unknown"]:
            if req_type in req_by_type and req_by_type[req_type]:
                with st.expander(f"{type_labels.get(req_type, req_type)} ({len(req_by_type[req_type])})", expanded=True if req_type == "FR" else False):
                    for req in req_by_type[req_type]:
                        st.markdown(f"""
                        **{req.get('category', 'General')}** [{req.get('priority', 'Medium')}]
                        
                        {req.get('description', 'No description')}
                        
                        *Status: {req.get('status', 'Draft')}*
                        
                        ---
                        """)
    else:
        st.info("No requirements collected yet.")

with col_chat:
    st.subheader(f"Project: {st.session_state.project_name}")
    st.caption(f"Domain: {st.session_state.domain}")
    
    # Conflict resolution UI
    if st.session_state.conflict_active:
        st.error("🚨 Requirement Conflict Detected!")
        st.write(st.session_state.conflict_details.get('conflict_details', 'Conflict found with existing requirement.'))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Keep Existing Requirement", use_container_width=True):
                # Resolve conflict by keeping existing
                st.session_state.conflict_active = False
                st.session_state.conflict_details = {}
                st.session_state.chat_history.append({
                    "role": "system",
                    "content": "User chose to keep the existing requirement."
                })
                st.rerun()
        
        with col2:
            if st.button("🆕 Keep New Input", use_container_width=True):
                # Resolve conflict by saving new requirement
                analysis = st.session_state.conflict_details.get('analysis')
                if analysis and st.session_state.project_id:
                    firebase_manager.save_requirement(
                        st.session_state.project_id,
                        analysis
                    )
                st.session_state.conflict_active = False
                st.session_state.conflict_details = {}
                st.rerun()
    
    # Chat interface
    st.divider()
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    if prompt := st.chat_input("Type your requirement here..."):
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.spinner("Analyzing requirement..."):
            # Agent 2: Analyze and detect conflicts
            analysis_result = ai_controller.analyze_and_detect_conflicts(
                prompt, 
                st.session_state.project_id
            )
            
            if analysis_result["conflict_detected"]:
                # Conflict detected - activate conflict mode
                st.session_state.conflict_active = True
                st.session_state.conflict_details = analysis_result
                
                # Agent 1: Ask for conflict resolution
                conflict_context = f"Conflict detected: {analysis_result['conflict_details']}"
                conflict_question = ai_controller.elicit_requirement(
                    st.session_state.domain,
                    conflict_context
                )
                
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": conflict_question
                })
                
            else:
                # No conflict - save requirement and continue
                if analysis_result["analysis"] and st.session_state.project_id:
                    firebase_manager.save_requirement(
                        st.session_state.project_id,
                        analysis_result["analysis"]
                    )
                
                # Agent 1: Ask next question
                next_question = ai_controller.elicit_requirement(st.session_state.domain)
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": next_question
                })
        
        st.rerun()

# Navigation
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("🔍 Analysis", use_container_width=True):
        st.switch_page("pages/3_Gap_Analysis.py")
with col3:
    if st.button("📄 Export", use_container_width=True):
        st.switch_page("pages/4_Export.py")