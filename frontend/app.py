import streamlit as st
from utils.api import signup, login, create_profile, get_profile

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

        with st.spinner("Logging in..."):
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

        with st.spinner("Creating account..."):
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

def profile_page():
    st.title("Your Fitness Profile 💪")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("Age", 10, 100, 25)
        weight = st.slider("Weight (kg)", 30, 300, 70)
        height_feet = st.selectbox("Height (feet)", [4, 5, 6, 7])
        height_inches = st.selectbox("Height (inches)", list(range(0, 12)))
    
    with col2:
        gender = st.selectbox("Gender", ["male", "female"])
        goal = st.selectbox("Goal", ["lose_weight", "gain_muscle", "maintain"])
        activity_level = st.selectbox("Activity Level", ["sedentary", "light", "moderate", "active"])

    if st.button("Save Profile", use_container_width=True):
        data = {
            "age": age,
            "weight": weight,
            "height_feet": height_feet,
            "height_inches": height_inches,
            "gender": gender,
            "goal": goal,
            "activity_level": activity_level
        }

        with st.spinner("Saving profile..."):
            response = create_profile(st.session_state["token"], data)

        if response.status_code == 200:
            st.session_state["profile"] = response.json()
            st.session_state["page"] = "dashboard"
            st.success("Profile saved!")
            st.rerun()
        else:
            try:
                detail = response.json().get("detail", "Failed to save profile")
            except:
                detail = "Failed to save profile"
            st.error(f"Failed to save profile: {detail}")

def dashboard_page():
    st.title("Dashboard 🏠")
    st.write(f"Welcome, {st.session_state['user']['name']}!")

    if st.session_state["profile"] is None:
        token = st.session_state["token"]

        with st.spinner("Loading profile..."):
            response = get_profile(token)

        if response.status_code == 200:
            st.session_state["profile"] = response.json()
        elif response.status_code == 404:
            st.warning("No profile found!")
            if st.button("Create Profile 💪", use_container_width=True):
                st.session_state["page"] = "profile"
                st.rerun()
            return
        else:
            st.error("Failed to load profile!")
            return

    profile = st.session_state["profile"]

    bmi = profile.get("bmi", 0)
    bmi_category = profile.get("bmi_category", "Unknown")

    if bmi_category == "Normal":
        bmi_color = "green"
    elif bmi_category == "Underweight":
        bmi_color = "orange"
    elif bmi_category == "Overweight":
        bmi_color = "orange"
    else:
        bmi_color = "red"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("BMI", f"{bmi:.1f}")
        st.markdown(f"<p style='color:{bmi_color};font-weight:bold;'>{bmi_category}</p>", unsafe_allow_html=True)
    with col2:
        st.metric("TDEE", f"{int(profile.get('tdee', 0))} kcal")
    with col3:
        st.metric("Goal", profile.get("goal", "maintain").replace("_", " ").title())

    st.subheader("Calorie Targets 🎯")
    tdee = profile.get("tdee", 0)
    cut = round(tdee - 500, 2)
    maintain = tdee
    bulk = round(tdee + 500, 2)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Cut ✂️", f"{cut} kcal")
    with col5:
        st.metric("Maintain ⚖️", f"{maintain} kcal")
    with col6:
        st.metric("Bulk 💪", f"{bulk} kcal")

    st.divider()
    st.subheader("Profile Details")
    c1, c2 = st.columns(2)
    c1.write(f"**Age:** {profile.get('age')} years")
    c1.write(f"**Weight:** {profile.get('weight')} kg")
    c2.write(f"**Gender:** {profile.get('gender', '').title()}")
    c2.write(f"**Activity:** {profile.get('activity_level', '').replace('_', ' ').title()}")

if st.session_state["token"] is None:
    auth_page = st.sidebar.radio("Navigation", ["Login", "Sign Up"])
    if auth_page == "Login":
        login_page()
    else:
        signup_page()
else:
    st.sidebar.title("NeuroFit AI 💪")
    st.sidebar.write(f"👤 {st.session_state['user']['name']}")
    st.sidebar.divider()

    nav = st.sidebar.radio("Navigation", ["Dashboard", "Profile"], 
                           index=0 if st.session_state["page"] == "dashboard" else 1)

    if nav == "Dashboard":
        st.session_state["page"] = "dashboard"
    elif nav == "Profile":
        st.session_state["page"] = "profile"

    st.sidebar.divider()
    if st.sidebar.button("Logout", use_container_width=True):
        logout()

    if st.session_state["page"] == "dashboard":
        dashboard_page()
    elif st.session_state["page"] == "profile":
        profile_page()
    else:
        dashboard_page()