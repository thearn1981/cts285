import streamlit as st

st.set_page_config(page_title="Citizen Portal", page_icon="🛰️")

st.title("Citizen Portal")

# ================== SESSION INITIALIZATION ==================

if "users" not in st.session_state:
    # { "username": {"password": "secret"} }
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# ================== DASHBOARD VIEW ==================

def show_dashboard():
    st.header("Citizen Dashboard")

    username = st.session_state.current_user
    st.write(f"Welcome, **{username}** 👋")

    # Mock metrics (static for this exercise)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Clearance Level", "α-3")
    with col2:
        st.metric("Missions Completed", "7")
    with col3:
        st.metric("Reputation Score", "92")

    st.write("---")
    if st.button("Logout"):
        # Clean logout: reset auth state
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.success("You have been safely logged out.")
        st.rerun()  # Refresh to show login/register again


# If already authenticated, show dashboard and stop
if st.session_state.logged_in:
    show_dashboard()
    st.stop()


# ================== AUTH TABS (LOGIN / REGISTER) ==================

tab_login, tab_register = st.tabs(["Login", "Register"])


# ----------- REGISTRATION FLOW -----------
with tab_register:
    st.subheader("Citizen Registration")

    # Let Streamlit clear the inputs when the form is successfully submitted
    with st.form("register_form", clear_on_submit=True):
        reg_username = st.text_input("Choose a username")
        reg_password = st.text_input("Choose a password", type="password")
        reg_confirm  = st.text_input("Confirm password", type="password")
        reg_submitted = st.form_submit_button("Register")

    if reg_submitted:
        username = reg_username.strip()
        password = reg_password
        confirm  = reg_confirm

        # --- Validation rules ---
        if not username:
            st.error("Username cannot be empty.")
        elif username in st.session_state.users:
            st.error("That username is already taken. Please choose another.")
        elif len(password) < 4:
            st.error("Password must be at least 4 characters long.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            st.session_state.users[username] = {"password": password}
            st.success(f"Citizen '{username}' registered successfully. You may now log in.")


# ----------- LOGIN FLOW -----------
with tab_login:
    st.subheader("Citizen Login")

    with st.form("login_form"):
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        login_submitted = st.form_submit_button("Login")

    if login_submitted:
        username = login_username.strip()
        password = login_password
        users = st.session_state.users

        # Basic checks
        if not username or not password:
            st.error("Please enter both username and password.")
        elif username not in users:
            st.error("No such citizen found. Please register first.")
        elif users[username]["password"] != password:
            st.error("Incorrect password. Access denied.")
        else:
            # Successful login: update session state
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success(f"Access granted. Welcome, {username}!")
            st.rerun()  # Immediately rerun to show the dashboard
