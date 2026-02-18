import streamlit as st
import pickle
import numpy as np
import pandas as pd
import time
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="HealthGuard Pro", layout="wide")

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
html, body, [class*="css"]{font-family:sans-serif;}

.stApp{
background:linear-gradient(120deg,#0f2027,#1a2a6c,#b21f1f,#fdbb2d);
background-size:300% 300%;
animation:holo 12s ease infinite;
color:white}

@keyframes holo{
0%{background-position:0%}
50%{background-position:100%}
100%{background-position:0%}
}

.card{
background:rgba(255,255,255,0.08);
padding:28px;
border-radius:20px;
box-shadow:0 10px 30px rgba(0,0,0,0.4)
}

.title{
font-size:55px;
font-weight:700;
text-align:center
}

.subtitle{
text-align:center;
color:#d1d1d1;
margin-bottom:15px
}

.stButton>button{
width:100%;
border-radius:12px;
height:45px;
font-weight:600;
background:linear-gradient(45deg,#00e0ff,#0072ff);
color:white
}

.fingerprint{
width:120px;height:120px;border-radius:50%;margin:auto;
border:3px solid #00eaff;
box-shadow:0 0 25px #00eaff88;
animation:scan 2s infinite
}

@keyframes scan{
0%{box-shadow:0 0 5px #00eaff}
50%{box-shadow:0 0 35px #00eaff}
100%{box-shadow:0 0 5px #00eaff}
}

.radar{
width:140px;height:140px;border-radius:50%;margin:auto;
border:2px solid #00ffaa;position:relative
}

.radar:before{
content:"";
position:absolute;width:100%;height:100%;
border-radius:50%;
background:conic-gradient(#00ffaa55 0deg,#0000 60deg);
animation:radar 2s linear infinite
}

@keyframes radar{
from{transform:rotate(0)}
to{transform:rotate(360deg)}
}

.typing{
font-size:20px;
border-right:3px solid #00eaff;
width:0;
overflow:hidden;
white-space:nowrap;
animation:typing 4s steps(40,end) forwards
}

@keyframes typing{
to{width:100%}
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

if "current_user" not in st.session_state:
    st.session_state.current_user=""

# ---------------- LOGIN PAGE ----------------
def login_page():

    st.markdown('<div class="title">HealthGuard</div>',unsafe_allow_html=True)
    st.markdown("<div class='fingerprint'></div>",unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI Medical Intelligence System</div>',unsafe_allow_html=True)

    left,center,right = st.columns([1,1.5,1])

    with center:
        st.markdown('<div class="card">',unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        col1,col2 = st.columns(2)

        with col1:
            login = st.button("Login")
        with col2:
            signup = st.button("Create Account")

        if signup:
            st.session_state.page="signup"
            st.rerun()

        if login:
            if username in st.session_state.users and st.session_state.users[username]==password:
                st.session_state.login=True
                st.session_state.current_user=username
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown('</div>',unsafe_allow_html=True)

# ---------------- SIGNUP ----------------
def signup_page():

    st.markdown('<div class="title">Create Account</div>',unsafe_allow_html=True)

    new_user=st.text_input("New Username")
    new_pass=st.text_input("New Password", type="password")

    if st.button("Sign Up"):
        if new_user in st.session_state.users:
            st.error("Username exists")
        else:
            st.session_state.users[new_user]=new_pass
            st.success("Account created")
            st.session_state.page="login"
            st.rerun()

    if st.button("Back"):
        st.session_state.page="login"
        st.rerun()

# ---------------- SIDEBAR ----------------
def sidebar():
    return st.sidebar.radio("Navigation",
    ["Dashboard","Diabetes","Heart","Tips","Logout"])

# ---------------- DASHBOARD ----------------
def dashboard():

    user=st.session_state.current_user

    st.title(f"Welcome {user} 👋")

    st.info("Small daily health decisions create big lifetime benefits.")

    st.markdown("### AI Diagnosis")
    st.markdown("<div class='typing'>Analyzing patient vitals...</div>",unsafe_allow_html=True)

    st.markdown("### Scan")
    st.markdown("<div class='radar'></div>",unsafe_allow_html=True)

    st.markdown("### Heart Monitor")
    pulse=np.sin(np.linspace(0,10,200))
    st.line_chart(pulse)

# ---------------- DIABETES ----------------
def diabetes():

    st.header("Diabetes Prediction")

    preg=st.number_input("Pregnancies",0)
    glucose=st.slider("Glucose",0,200,100)
    bp=st.slider("Blood Pressure",0,150,70)
    skin=st.slider("Skin Thickness",0,100,20)

    insulin=st.slider("Insulin",0,900,80)
    height=st.number_input("Height (m)",1.0,2.5)
    weight=st.number_input("Weight (kg)",20.0,200.0)
    age=st.slider("Age",1,100,25)
    dpf=st.number_input("DPF",0.0)

    bmi=weight/(height**2)
    st.success(f"BMI: {bmi:.2f}")

    if st.button("Analyze"):
        if diabetes_model:
            data=np.array([[preg,glucose,bp,skin,insulin,bmi,dpf,age]])
            prob=diabetes_model.predict_proba(data)[0][1]*100
            st.progress(int(prob))
            st.write(f"Risk {prob:.2f}%")
        else:
            st.error("Model missing")

# ---------------- HEART ----------------
def heart():

    st.header("Heart Disease Prediction")

    age=st.number_input("Age",20,100,40)
    chol=st.number_input("Cholesterol",100,400,200)
    hr=st.number_input("Max Heart Rate",60,220,150)

    if st.button("Analyze"):
        if heart_model:
            data=np.array([[age,1,0,120,chol,0,0,hr,0,1,0,0,1]])
            prob=heart_model.predict_proba(data)[0][1]*100
            st.progress(int(prob))
            st.write(f"Risk {prob:.2f}%")
        else:
            st.error("Model missing")

# ---------------- TIPS ----------------
def tips():
    tips=[
        "Exercise daily",
        "Sleep well",
        "Drink water",
        "Avoid junk food",
        "Regular checkups"
    ]
    for t in tips:
        st.success(t)

# ---------------- LOGOUT ----------------
def logout():
    st.session_state.login=False
    st.rerun()

# ---------------- MAIN ----------------
if not st.session_state.login:

    if st.session_state.page=="login":
        login_page()
    else:
        signup_page()

else:

    page=sidebar()

    if page=="Dashboard": dashboard()
    elif page=="Diabetes": diabetes()
    elif page=="Heart": heart()
    elif page=="Tips": tips()
    elif page=="Logout": logout()
