import streamlit as st
import pickle
import numpy as np
import pandas as pd
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="HealthGuard Pro", layout="wide")

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(to right,#0f2027,#203a43,#2c5364);
    color:white;
}

.card {
    background:#ffffff10;
    padding:25px;
    border-radius:18px;
    box-shadow:0 8px 25px rgba(0,0,0,0.3);
    backdrop-filter: blur(6px);
}

.title {
    font-size:42px;
    font-weight:600;
    text-align:center;
}

.subtitle {
    text-align:center;
    font-size:18px;
    color:#d1d1d1;
}

.stButton>button {
    width:100%;
    border-radius:10px;
    height:45px;
    font-size:16px;
    font-weight:600;
    background:linear-gradient(to right,#00c6ff,#0072ff);
    color:white;
    border:none;
}

.stButton>button:hover {
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODELS ----------------
try:
    diabetes_model = pickle.load(open("model.pkl","rb"))
    heart_model = pickle.load(open("heart_model.pkl","rb"))
except:
    diabetes_model=None
    heart_model=None

# ---------------- SESSION STATE ----------------
if "login" not in st.session_state:
    st.session_state.login=False

if "users" not in st.session_state:
    st.session_state.users={"admin":"1234"}

if "page" not in st.session_state:
    st.session_state.page="login"


# ---------------- LOGIN PAGE ----------------
def login_page():
    st.markdown('<div class="title">HealthGuard Pro</div>',unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI Health Risk Prediction System</div>',unsafe_allow_html=True)
    st.write("")

    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username=="admin" and password=="1234":
                st.session_state.login=True
                st.success("Login successful")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown('</div>',unsafe_allow_html=True)


# ---------------- SIDEBAR MENU ----------------
def sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to",
        ["Dashboard","Diabetes Prediction","Heart Prediction","Health Tips","Logout"])
    return page


# ---------------- DASHBOARD ----------------
def dashboard():
    st.markdown("## Dashboard Overview")

    col1,col2,col3 = st.columns(3)

    col1.metric("Global Diabetes","537 Million")
    col2.metric("Heart Deaths","20 Million/yr")
    col3.metric("Model Accuracy","~88%")

    st.write("")
    st.info("Select a module from sidebar to begin analysis.")


# ---------------- DIABETES MODULE ----------------
def diabetes():
    st.markdown("## Diabetes Risk Prediction")

    col1,col2 = st.columns(2)

    with col1:
        preg = st.number_input("Pregnancies",0)
        glucose = st.slider("Glucose",0,200,100)
        bp = st.slider("Blood Pressure",0,150,70)
        skin = st.slider("Skin Thickness",0,100,20)

    with col2:
        insulin = st.slider("Insulin",0,900,80)
        height = st.number_input("Height (m)",1.0,2.5)
        weight = st.number_input("Weight (kg)",20.0,200.0)
        age = st.slider("Age",1,100,25)
        dpf = st.number_input("DPF",0.0)

    bmi = weight/(height**2)
    st.success(f"BMI: {bmi:.2f}")

    if st.button("Analyze Diabetes Risk"):
        if diabetes_model is None:
            st.error("Model not loaded")
        else:
            data = np.array([[preg,glucose,bp,skin,insulin,bmi,dpf,age]])
            prob = diabetes_model.predict_proba(data)[0][1]*100

            st.progress(int(prob))
            st.subheader(f"Risk: {prob:.2f}%")

            if prob<30:
                st.success("Low Risk")
            elif prob<70:
                st.warning("Moderate Risk")
            else:
                st.error("High Risk")


# ---------------- HEART MODULE ----------------
def heart():
    st.markdown("## Heart Disease Prediction")

    age = st.slider("Age",20,100,40)
    sex = st.selectbox("Gender",[0,1])
    cp = st.slider("Chest Pain Type",0,3,1)
    chol = st.slider("Cholesterol",100,400,200)
    maxhr = st.slider("Max Heart Rate",60,220,150)
    oldpeak = st.slider("ST Depression",0.0,6.0,1.0)

    if st.button("Analyze Heart Risk"):
        if heart_model is None:
            st.error("Model not loaded")
        else:
            data=np.array([[age,sex,cp,120,chol,0,0,maxhr,0,oldpeak,0,0,1]])
            prob=heart_model.predict_proba(data)[0][1]*100

            st.progress(int(prob))
            st.subheader(f"Risk: {prob:.2f}%")

            if prob<30:
                st.success("Low Risk")
            elif prob<70:
                st.warning("Moderate Risk")
            else:
                st.error("High Risk")


# ---------------- HEALTH TIPS MODULE ----------------
def tips():
    st.markdown("## Smart Health Tips")

    tips_list=[
        "Exercise at least 30 minutes daily",
        "Avoid excess sugar intake",
        "Sleep minimum 7 hours",
        "Drink enough water",
        "Regular medical checkups"
    ]

    for tip in tips_list:
        st.success(tip)


# ---------------- LOGOUT ----------------
def logout():
    st.session_state.login=False
    st.rerun()


# ---------------- SIGNUP PAGE ----------------
def signup_page():
    st.markdown('<div class="title">Create Account</div>',unsafe_allow_html=True)
    st.write("")

    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)

        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Sign Up"):
            if new_user in st.session_state.users:
                st.error("Username already exists")
            elif new_user=="" or new_pass=="":
                st.warning("Enter valid details")
            else:
                st.session_state.users[new_user]=new_pass
                st.success("Account created successfully")
                time.sleep(1)
                st.session_state.page="login"
                st.rerun()

        if st.button("Back to Login"):
            st.session_state.page="login"
            st.rerun()

        st.markdown('</div>',unsafe_allow_html=True)


# ---------------- MAIN CONTROL ----------------
if not st.session_state.login:
    if st.session_state.page=="login":
        login_page()
        if st.button("Create new account"):
            st.session_state.page="signup"
            st.rerun()
    else:
        signup_page()
else:
    page=sidebar()

    if page=="Dashboard": dashboard()
    elif page=="Diabetes Prediction": diabetes()
    elif page=="Heart Prediction": heart()
    elif page=="Health Tips": tips()
    elif page=="Logout": logout()
