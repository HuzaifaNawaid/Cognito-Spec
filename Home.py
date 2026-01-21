import streamlit as st

# --- 1. HIDE DEFAULT NAVIGATION CSS INJECTION ---
# Targets the automatically generated navigation div and hides it
st.markdown("""
<style>
/* Hides the default Streamlit sidebar navigation menu */
div[data-testid="stSidebarNav"] {
    display: none;
}

/* --- GENERAL WORKFLOW CARD STYLES --- */
.card-container {
    display: flex;
    flex-direction: column;
    gap: 2rem; /* Increased gap between rows */
    margin-top: 2rem;
}
.styled-card {
    background-color: var(--secondary-background-color);
    border: 1px solid #4a148c; /* Darker Purple Border */
    border-radius: 1rem;
    padding: 2rem;
    transition: all 0.3s ease;
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2); /* Enhanced Shadow */
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: flex-start; /* Align content to top */
    height: 280px; /* INCREASED HEIGHT for better content fit */
    margin-bottom: 0.5rem; 
}
.styled-card:hover {
    transform: translateY(-5px);
    border-color: #6b21a8; 
    box-shadow: 0 12px 20px rgba(107, 33, 168, 0.5); 
}
.card-title {
    /* *** ADJUSTED FONT SIZE - slightly smaller but still stylish *** */
    font-size: 2rem; /* Reduced from 2.5rem for better fit */
    font-weight: 900;
    color: #3b82f6; /* Bright Blue Title */
    margin-bottom: 0.5rem;
    /* Added text shadow similar to the main header */
    text-shadow: 0 0 5px rgba(59, 130, 246, 0.5); 
    /* Added gradient effect for extra style */
    background: linear-gradient(45deg, #3b82f6, #8b5cf6, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.5px;
    line-height: 1.2;
}
.card-description {
    color: var(--text-color);
    opacity: 0.9; 
    font-size: 1.1rem; /* Slightly reduced from 1.25rem */
    flex-grow: 1; 
    font-weight: 400;
    line-height: 1.5;
    /* Added subtle text shadow for better readability */
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    margin-top: 0.5rem;
}
.card-icon {
    font-size: 4rem; /* Slightly reduced from 4.5rem */
    color: #8b5cf6; /* Light Purple for Icons */
    margin-bottom: 0.5rem;
    display: block;
    /* Added subtle text shadow to icons */
    text-shadow: 0 0 8px rgba(139, 92, 246, 0.3);
}

/* --- REMOVED BUTTON STYLES (No buttons rendered) --- */
.external-action-btn, .card-action-btn {
    display: none !important;
}

/* --- PROMINENT MAIN HEADER CARD (The glowing card) --- */
.main-header-card {
    background-color: var(--secondary-background-color);
    border-radius: 1rem;
    padding: 3rem 2rem;
    transition: all 0.5s ease-in-out;
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 3rem;
    position: relative;
    overflow: hidden;
    /* Removed cursor: pointer as the card is no longer clickable */
    box-shadow: 0 0 50px rgba(59, 130, 246, 0.3), 
                0 0 30px rgba(107, 33, 168, 0.3); 
}
.main-header-card:before {
    content: '';
    position: absolute;
    top: -5px; left: -5px; right: -5px; bottom: -5px;
    background: linear-gradient(45deg, #3b82f6, #6b21a8, #3b82f6);
    z-index: -1;
    border-radius: 1.2rem;
    filter: blur(8px);
    opacity: 0.7;
    transition: opacity 0.5s ease;
}

.main-header-card:hover {
    transform: translateY(-5px) scale(1.005);
    box-shadow: 0 0 60px rgba(59, 130, 246, 0.5), 
                0 0 40px rgba(107, 33, 168, 0.5);
}

.main-header-title {
    font-size: 2.75rem;
    font-weight: 900;
    color: #3b82f6; 
    margin-bottom: 0.5rem;
    text-shadow: 0 0 10px rgba(59, 130, 246, 0.7);
    background: linear-gradient(45deg, #3b82f6, #8b5cf6, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.5px;
}
.main-header-subtitle {
    color: var(--text-color);
    opacity: 0.9;
    font-size: 1.25rem;
    margin-bottom: 0; 
    font-weight: 400;
    line-height: 1.5;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* --- WORKFLOW CARD CONTAINER STYLING --- */
.workflow-card-container {
    display: flex;
    flex-direction: column;
    gap: 2rem; /* Increased gap between rows */
    margin-top: 2rem;
}

/* --- SPECIAL STYLING FOR THE 4TH CARD (SRS Generation) --- */
.card-special {
    background-color: var(--secondary-background-color);
    border: 1px solid #3b82f6; /* Blue border for special emphasis */
    border-radius: 1rem;
    padding: 2rem;
    transition: all 0.3s ease;
    box-shadow: 0 8px 15px rgba(59, 130, 246, 0.2); /* Blue-tinted shadow */
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 280px; /* INCREASED HEIGHT to match other cards */
    margin-bottom: 0.5rem;
}
.card-special:hover {
    transform: translateY(-5px);
    border-color: #2563eb; 
    box-shadow: 0 12px 20px rgba(59, 130, 246, 0.4); 
}
.card-special-title {
    font-size: 2rem; /* Reduced from 2.5rem to match other cards */
    font-weight: 900;
    color: #3b82f6;
    margin-bottom: 0.5rem;
    text-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
    background: linear-gradient(45deg, #3b82f6, #60a5fa, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.5px;
    line-height: 1.2;
}
.card-special-description {
    color: var(--text-color);
    opacity: 0.9; 
    font-size: 1.1rem; /* Slightly reduced from 1.25rem */
    flex-grow: 1; 
    font-weight: 400;
    line-height: 1.5;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    margin-top: 0.5rem;
}

/* --- FOR THE TWO CARD ROWS --- */
.two-card-row {
    display: flex;
    justify-content: center;
    gap: 2rem; /* Space between the two cards */
    margin-bottom: 2rem;
}

/* Ensure each card takes equal width in the two-card layout */
.two-card-col {
    flex: 1;
    min-width: 0; /* Important for equal width distribution */
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

# Initialize session state with default values
def initialize_session_state():
    default_values = {
        'project_initialized': False,
        'project_id': None,
        'project_name': "",
        'domain': "Healthcare",
        'chat_history': [],
        'conflict_active': False,
        'conflict_details': {},
        'requirements': [],
        'current_question': ""
    }
    
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# --- CUSTOM SELECTION BOX NAVIGATION LOGIC ---
def navigate_with_selectbox(current_page_name):
    """Handles the sidebar selectbox navigation and switches pages."""
    
    page_names = {
        "🏠 Home": "Home.py",
        "⚙️ 1. Project Setup": "pages/1_Project_Setup.py",
        "💬 2. Interview": "pages/2_Interview.py",
        "🔍 3. Gap Analysis": "pages/3_Gap_Analysis.py",
        "📄 4. SRS Generation": "pages/4_Export.py"
    }
    
    selected_page_name = st.selectbox(
        "**Go to Page:**", 
        options=list(page_names.keys()), 
        index=list(page_names.keys()).index(current_page_name),
        key=f"custom_sidebar_select_{current_page_name.replace(' ', '_')}" 
    )

    # Switch page only if a different option is selected
    if selected_page_name != current_page_name:
        st.switch_page(page_names[selected_page_name])

# Sidebar content
with st.sidebar:
    # Sidebar logo/Title
    try:
        # Assuming 'logooo.png' is available
        st.image("logooo.png", width=270) 
    except:
        st.title("🚀 Cognito-Spec") 

    st.markdown("---")
    
    # Custom Navigation Selectbox
    navigate_with_selectbox("🏠 Home")
    
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

# Function to create a workflow card (Now only displays the card content)
def create_card(column, icon, title, description, special_card=False):
    with column:
        if special_card:
            # Special styling for the 4th card (SRS Generation)
            st.markdown(
                f"""
                <div class="card-special">
                    <span class="card-icon">{icon}</span>
                    <div class="card-special-title">{title}</div>
                    <div class="card-special-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Standard styling for other cards
            st.markdown(
                f"""
                <div class="styled-card">
                    <span class="card-icon">{icon}</span>
                    <div class="card-title">{title}</div>
                    <div class="card-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Function to render the main glowing header card (Now static)
def render_main_header_card():
    # The main card structure - card is purely decorative
    st.markdown(
        f"""
        <div class="main-header-card">
            <div class="main-header-title">Cognito-Spec: Powered by a Team of Four Autonomous AI Analysts.</div>
            <div class="main-header-subtitle">Harness a multi-agent system that works like a full RE team, ensuring every requirement is captured, clarified, structured, and validated without the usual gaps or inconsistencies.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()

# Main app
def main():
    # 1. Glowing Header Card (Static Display)
    render_main_header_card()
    
    st.header("Start Your Workflow")

    # Use a container for the custom card CSS to take effect
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    
    # Row 1: First pair of cards (Setup and Interview)
    st.markdown('<div class="two-card-row">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    # Card 1: Setup
    create_card(
        col1, 
        icon="⚙️", 
        title="1. Project Setup", 
        description="Define your project name and industry domain to configure the AI engineer."
    )

    # Card 2: Interview
    create_card(
        col2, 
        icon="💬", 
        title="2. Requirement Interview", 
        description="Engage in a structured chat with the AI Agent to elicit requirements iteratively."
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Second pair of cards (Gap Analysis and SRS Generation)
    st.markdown('<div class="two-card-row">', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    
    # Card 3: Gap Analysis
    create_card(
        col3, 
        icon="🔍", 
        title="3. Gap Analysis", 
        description="Validate collected requirements and identify missing functional or non-functional needs."
    )

    # Card 4: SRS Generation (Special card)
    create_card(
        col4, 
        icon="📄", 
        title="4. SRS Generation", 
        description="Automatically compile all confirmed requirements into a professional SRS document.",
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()

    # Check for initialization status and show setup button if needed
    if not st.session_state.project_initialized:
        if st.button("▶️ Initialize New Project", type="primary", use_container_width=True):
            st.switch_page("pages/1_Project_Setup.py")
        st.divider()
    
    # Status message if a project is not initialized
    if not st.session_state.project_initialized:
        st.info("Click the **Initialize New Project** button above or navigate to **Project Setup** in the sidebar to begin your requirements journey!")


if __name__ == "__main__":
    st.session_state.current_page = "🏠 Home"
    main()