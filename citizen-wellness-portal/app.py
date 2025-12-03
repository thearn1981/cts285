import streamlit as st
import sqlite3

# --- helper function: check username + password in DB ---
def check_login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Look for a user with this username and password
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()

    conn.close()
    return user is not None


# --- Streamlit app starts here ---
st.title("Simple Login")

# 1) Username & password inputs
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# 2) Login button
if st.button("Login"):
    # 3) When clicked, check database
    if check_login(username, password):
        st.success("Login successful! 🎉")
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
    else:
        st.error("Invalid username or password")
        

# 4) If user is logged in, show a welcome message
if st.session_state.get("logged_in"):
    st.write(f"Welcome, {st.session_state['username']}!")
