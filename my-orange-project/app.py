import streamlit as st
import sqlite3
import calendar
import datetime as dt
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Citizen Portal", page_icon="🛰️")

st.title("Citizen Portal")

# ================== DATABASE HELPERS ==================

DB_NAME = "citizens.db"


def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    """Create the users table if it does not already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def user_exists(username: str) -> bool:
    """Check if a username is already in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row is not None


def create_user(username: str, password: str) -> None:
    """Insert a new user into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password),
    )
    conn.commit()
    conn.close()


def validate_login(username: str, password: str) -> bool:
    """Return True if the username/password pair is valid."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False

    stored_password = row[0]
    return stored_password == password


# Initialize DB
init_db()

# ================== SESSION INITIALIZATION ==================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# ================== THEME HELPERS ==================

def shared_soft_styles():
    """Styles shared between login and dashboard to soften widgets/cards."""
    st.markdown(
        """
        <style>
        /* Glass card container */
        .glass-card {
            background: rgba(255, 255, 255, 0.7);
            border-radius: 18px;
            padding: 1.5rem 1.75rem;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(14px);
        }

        .glass-card h1,
        .glass-card h2,
        .glass-card h3,
        .glass-card h4 {
            color: #50304f;
        }

        /* Soften text/password inputs */
        .stTextInput > div > div > input,
        .stPasswordInput > div > div > input {
            border-radius: 999px !important;
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
            background-color: rgba(255, 255, 255, 0.95) !important;
            padding: 0.45rem 0.9rem !important;
        }

        /* Soften buttons */
        .stButton > button {
            border-radius: 999px !important;
            border: none;
            padding: 0.5rem 1.4rem;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
            background: linear-gradient(135deg, #ffb6d9, #ffd6e8);
            color: #50304f;
            font-weight: 600;
        }

        .stButton > button:hover {
            filter: brightness(1.04);
            transform: translateY(-1px);
        }

        /* Slightly soften tab labels */
        div[data-baseweb="tab"] {
            border-radius: 999px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def set_login_theme():
    """Pastel pink background with clouds and a warm sunbeam."""
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(
                180deg,
                rgba(255, 215, 235, 0.9) 0%,
                rgba(255, 230, 240, 0.9) 40%,
                rgba(255, 240, 245, 0.9) 100%
            ),
            url('https://cdn.pixabay.com/photo/2016/11/18/16/51/cloud-1839700_1280.png'); /* soft clouds background */
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .sunbeam {
            position: fixed;
            top: -80px;
            left: -80px;
            width: 420px;
            height: 420px;
            background: radial-gradient(
                circle,
                rgba(255, 255, 200, 0.55) 0%,
                rgba(255, 255, 200, 0.15) 40%,
                rgba(255, 255, 200, 0) 70%
            );
            filter: blur(20px);
            pointer-events: none;
            z-index: -1;
        }
        </style>

        <div class="sunbeam"></div>
        """,
        unsafe_allow_html=True,
    )
    shared_soft_styles()


def set_dashboard_theme():
    """Mint green background for the logged-in dashboard."""
    pastel_mint = "#CFFFE5"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {pastel_mint} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    shared_soft_styles()


# ================== DASHBOARD VIEW ==================

def show_dashboard():
    # Apply mint green background + soft widgets for logged-in view
    set_dashboard_theme()

    # Start glass card wrapper
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.header("Citizen Dashboard")

    username = st.session_state.current_user or "Citizen"
    st.write(f"Welcome, **{username}** 👋")

    # ---------- Mission Calendar ----------
    st.subheader("Mission Calendar")

    # --- Get current year & month (you can also hardcode these) ---
    today = dt.datetime.now(ZoneInfo("America/New_York")).date()
    year = today.year
    month = today.month

    # --- For a specific month instead, you could do: ---
    # year = 2025
    # month = 3  # March

    # --- Create a calendar object (Sunday-first or Monday-first) ---
    cal = calendar.Calendar(firstweekday=6)  # 6 = Sunday, 0 = Monday

    month_name = calendar.month_name[month]
    st.write(f"**{month_name} {year}**")

    # --- Day-of-week headers ---
    dow_cols = st.columns(7)
    for col, name in zip(dow_cols, ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
        with col:
            st.markdown(
                "<div style='text-align:center; font-weight:600;'>"
                + name +
                "</div>",
                unsafe_allow_html=True,
            )

    st.write("")  # little spacer

    # --- Weeks in this month (each 'week' is a list of 7 day numbers, 0 = no day) ---
    weeks = cal.monthdayscalendar(year, month)

    for week in weeks:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    # empty cell for days not in this month
                    st.markdown(
                        "<div style='height:60px;'></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    # Highlight today's date
                    is_today = (year == today.year and month == today.month and day == today.day)

                    border_color = "black" if is_today else "rgba(255,255,255,0.8)"
                    border_width = "2px" if is_today else "1px"

                    st.markdown(
                        f"""
                        <div style="
                            height:60px;
                            border-radius:12px;
                            border:{border_width} solid {border_color};
                            background: rgba(255,255,255,0.75);
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            box-shadow: 0 6px 14px rgba(0,0,0,0.06);
                            font-weight:600;
                            color:#50304f;
                        ">
                            {day}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


    # ---------- Metrics under the calendar ----------
    st.write("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Clearance Level", "α-3")
    with col2:
        st.metric("Missions Completed", "7")
    with col3:
        st.metric("Reputation Score", "92")

    st.write("")

    # ---------- Logout button ----------
    if st.button("Logout"):
        # Clean logout: reset auth state
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.success("You have been safely logged out.")
        st.rerun()  # Refresh to show login/register again

    # Close glass card wrapper
    st.markdown("</div>", unsafe_allow_html=True)

    

# ================== ROUTING: DASHBOARD vs AUTH ==================

# If already authenticated, show dashboard and stop
if st.session_state.logged_in:
    show_dashboard()
    st.stop()

# If NOT logged in, apply login/register theme
set_login_theme()

# ================== AUTH TABS (LOGIN / REGISTER) ==================

tab_login, tab_register = st.tabs(["Login", "Register"])

# ----------- REGISTRATION FLOW -----------
with tab_register:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.subheader("Citizen Registration")

    # Let Streamlit clear the inputs when the form is successfully submitted
    with st.form("register_form", clear_on_submit=True):
        reg_username = st.text_input("Choose a username")
        reg_password = st.text_input("Choose a password", type="password")
        reg_confirm = st.text_input("Confirm password", type="password")
        reg_submitted = st.form_submit_button("Register")

    if reg_submitted:
        username = reg_username.strip()
        password = reg_password
        confirm = reg_confirm

        # --- Validation rules ---
        if not username:
            st.error("Username cannot be empty.")
        elif user_exists(username):
            st.error("That username is already taken. Please choose another.")
        elif len(password) < 4:
            st.error("Password must be at least 4 characters long.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            create_user(username, password)
            st.success(f"Citizen '{username}' registered successfully. You may now log in.")

    st.markdown("</div>", unsafe_allow_html=True)


# ----------- LOGIN FLOW -----------
with tab_login:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.subheader("Citizen Login")

    with st.form("login_form"):
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        login_submitted = st.form_submit_button("Login")

    if login_submitted:
        username = login_username.strip()
        password = login_password

        # Basic checks
        if not username or not password:
            st.error("Please enter both username and password.")
        elif not user_exists(username):
            st.error("No such citizen found. Please register first.")
        elif not validate_login(username, password):
            st.error("Incorrect password. Access denied.")
        else:
            # Successful login: update session state
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success(f"Access granted. Welcome, {username}!")
            st.rerun()  # Immediately rerun to show the dashboard

    st.markdown("</div>", unsafe_allow_html=True)


