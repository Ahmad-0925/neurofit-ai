import streamlit as st
from utils.api import signup, login

st.set_page_config(page_title="NeuroFit AI", page_icon="💪")

if "token" not in st.session_state:
    st.session_state["token"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "user" not in st.session_state:
    st.session_state["user"] = None
if "profile" not in st.session_state:
    st.session_state["profile"] = None

def logout():
    st.session_state["token"] = None
    st.session_state["user"] = None
    st.session_state["profile"] = None
    st.session_state["page"] = "login"
    st.rerun()

def login_page():
    st.title("Welcome to NeuroFit AI 💪")
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if not email or not password:
            st.error("Please fill in all fields.")
            return

        response = login(email, password)
        if response.status_code == 200:
            data = response.json()
            st.session_state["token"] = data["access_token"]
            st.session_state["user"] = {"name": data.get("name", "User"), "email": email}
            st.session_state["page"] = "dashboard"
            st.success("Login successful!")
            st.rerun()
        elif response.status_code == 401:
            st.error("Invalid email or password!")
        else:
            try:
                detail = response.json().get("detail", "Login failed")
            except:
                detail = "Login failed"
            st.error(f"Login failed: {detail}")

def signup_page():
    st.title("Welcome to NeuroFit AI 💪")
    st.subheader("Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pass")

    if st.button("Sign Up", use_container_width=True):
        if not name or not email or not password:
            st.error("Please fill in all fields.")
            return

        response = signup(name, email, password)
        if response.status_code == 200:
            data = response.json()
            st.session_state["token"] = data["access_token"]
            st.session_state["user"] = {"name": name, "email": email}
            st.session_state["page"] = "dashboard"
            st.success("Account created! Logging you in...")
            st.rerun()
        elif response.status_code == 400:
            st.error("Signup failed! Email may already exist.")
        else:
            try:
                detail = response.json().get("detail", "Signup failed")
            except:
                detail = "Signup failed"
            st.error(f"Signup failed: {detail}")

def dashboard_page():
    st.title("Dashboard 🏠")
    st.write(f"Welcome, {st.session_state['user']['name']}!")
    st.info("Profile and metrics will appear here in later modules.")

    if st.button("Logout"):
        logout()

if st.session_state["token"] is None:
    auth_page = st.sidebar.radio("Navigation", ["Login", "Sign Up"])
    if auth_page == "Login":
        login_page()
    else:
        signup_page()
else:
    if st.session_state["page"] == "login":
        st.session_state["page"] = "dashboard"
        st.rerun()
    elif st.session_state["page"] == "dashboard":
        dashboard_page()
    elif st.session_state["page"] == "profile":
        st.write("Profile form will go here (Module 4)")
    else:
        dashboard_page()