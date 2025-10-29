"""
Datamon - Streamlit Version

A math problem helper that helps students, teachers and parents
make math fun.

Haylee Kaheel Teresa Aryan Justin
"""

import streamlit as st
from AnswerChecker_streamlit import answer_checker_page

# Configure the page
st.set_page_config(
    page_title="Datamon Math Helper",
    page_icon="🧮",
    layout="centered"
)

# Initialize session state for points and current page
if 'player_points' not in st.session_state:
    st.session_state.player_points = 0

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'menu'

def show_menu():
    """Display the main menu"""
    st.title("🧮 Datamon Math Helper")
    st.markdown("---")
    
    # Display current points prominently
    st.metric(label="Total Points", value=st.session_state.player_points)
    
    st.markdown("### Choose Your Challenge:")
    
    # Create buttons for each option
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Answer Checker", use_container_width=True):
            st.session_state.current_page = 'answer_checker'
            st.rerun()
    
    with col2:
        if st.button("🧠 Memory Bank", use_container_width=True):
            st.info("Coming soon!")
            # st.session_state.current_page = 'memory_bank'
            # st.rerun()
    
    with col3:
        if st.button("⚡ Electro Flash", use_container_width=True):
            st.info("Coming soon!")
            # st.session_state.current_page = 'electro_flash'
            # st.rerun()
    
    st.markdown("---")
    st.markdown("**How to play:** Select a game mode above to start earning points!")

def main():
    """Main application logic"""
    
    # Show different pages based on current_page state
    if st.session_state.current_page == 'menu':
        show_menu()
    
    elif st.session_state.current_page == 'answer_checker':
        answer_checker_page()
    
    # Add other game modes here as elif statements
    # elif st.session_state.current_page == 'memory_bank':
    #     memory_bank_page()
    
    # elif st.session_state.current_page == 'electro_flash':
    #     electro_flash_page()

if __name__ == "__main__":
    main()
