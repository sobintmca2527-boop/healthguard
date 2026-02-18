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

html, body, [class*="css"]{font-family:'Poppins',sans-serif;}

.stApp{background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);color:white}

.card{background:rgba(255,255,255,0.08);padding:28px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.4);backdrop-filter:blur(10px);animation:fadeIn .8s}
@keyframes fadeIn{from{opacity:0;transform:translateY(15px)}to{opacity:1;transform:translateY(0)}}

.title{font-size:58px;font-weight:700;text-align:center;letter-spacing:1px;animation:fadeIn 1s ease}
.subtitle{text-align:center;color:#d1d1d1;margin-bottom:15px}

/* Sidebar */
section[data-testid="stSidebar"]{background:#0a1a24}
section[data-testid="stSidebar"] .stRadio label{padding:8px;border-radius:10px;transition:.3s}
section[data-testid="stSidebar"] .stRadio label:hover{background:#00c6ff22;transform:translateX(5px)}

/* Inputs */
div[data-baseweb="input"] input{background:transparent!important;border:1px solid rgba(255,255,255,.3)!important;border-radius:12px!important;padding:12px!important;color:white!important}
div[data-baseweb="input"] input:focus{border:1px solid #00e0ff!important;box-shadow:0 0 10px #00e0ff55}

/* Buttons */
.stButton>button{width:100%;border:none;border-radius:12px;height:48px;font-weight:600;font-size:16px;color:white;background:linear-gradient(45deg,#00e0ff,#0072ff,#00c6ff);background-size:200% 200%;animation:gradientMove 4s ease infinite}
@keyframes gradientMove{0%{background-position:0%}50%{background-position:100%}100%{background-position:0%}}
.stButton>button:hover{transform:scale(1.03)}

label{font-weight:500!important;color:#e8f6ff!important}
img.header{display:block;margin:auto;width:180px;filter:drop-shadow(0 0 15px #00e0ff88);animation:float 3s ease-in-out infinite}
@keyframes float{0%{transform:translateY(0)}50%{transform:translateY(-12px)}100%{transform:translateY(0)}}

.card:hover{transform:scale(1.02);transition:.4s}

/* Neumorphism Cards */
.neo{
background:#e0e5ec22;
border-radius:20px;
box-shadow:8px 8px 18px #00000055,-8px -8px 18px #ffffff22;
padding:25px;
animation:fadeIn 1s}

/* Heartbeat animation */
@keyframes beat{0%{transform:scale(1)}25%{transform:scale(1.08)}40%{transform:scale(1)}60%{transform:scale(1.08)}100%{transform:scale(1)}}
.beat{animation:beat 1.2s infinite;color:#ff4b5c;font-size:28px;text-align:center}

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
    st.markdown("<img class='header' src='https://cdn-icons-png.flaticon.com/512/2966/2966485.png'>",unsafe_allow_html=True)
    st.markdown('<div class="title">HealthGuard</div>',unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI Medical Intelligence System</div>',unsafe_allow_html=True)
    st.write("")

    left,center,right = st.columns([1.2,1.5,1.2])

    with center:
        st.markdown('<div class="card">',unsafe_allow_html=True)
        st.markdown("### 🔐 Secure Login")
        btn1,btn2=st.columns(2)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        st.write("")
        with btn1:
            login_click = st.button("Login")
        with btn2:
            signup_click = st.button("Create Account")

        if signup_click:
            st.session_state.page="signup"
            st.rerun()

        if login_click:
            if username in st.session_state.users and st.session_state.users[username]==password:
                st.session_state.login=True
                st.success("Login successful")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown('</div>',unsafe_allow_html=True)


# ---------------- SIDEBAR MENU ----------------
def sidebar():
    st.sidebar.markdown("## 🧭 Navigation")

    theme = st.sidebar.toggle("🌙 Dark Mode",value=True)
    if not theme:
        st.markdown("""
        <style>
        .stApp{background:#f5f7fb;color:black}
        </style>
        """,unsafe_allow_html=True)

    page = st.sidebar.radio("",
        ["🏠 Dashboard","🧪 Diabetes Prediction","❤️ Heart Prediction","💡 Health Tips","🚪 Logout"])
    return page


# ---------------- TYPING HEADER ----------------
def header_image():
    st.markdown("<img class='header' src='https://cdn-icons-png.flaticon.com/512/3774/3774299.png'>",unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;font-size:52px'>HealthGuard AI Dashboard</h1>",unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
def dashboard():
    header_image()

    c1,c2,c3=st.columns(3)
    c1.markdown("<div class='neo'><h3>🩺 Stay Healthy</h3><p>Prevention is better than cure. Monitor your health regularly.</p></div>",unsafe_allow_html=True)
    c2.markdown("<div class='neo'><h3>💊 Reminders</h3><p>Take medicines on time and maintain diet discipline.</p></div>",unsafe_allow_html=True)
    c3.markdown("<div class='neo'><h3>🏃 Motivation</h3><p>Daily activity + good sleep = strong heart & mind.</p></div>",unsafe_allow_html=True)

    st.write("")
    st.markdown("### ❤️ Health Status Indicator")
    st.markdown("<div class='beat'>♥ Monitoring Active</div>",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🧾 Personal & Medical Profile")

    col1,col2=st.columns(2)

    with col1:
        st.markdown("### 👤 Personal Details")
        name=st.text_input("Full Name")
        age=st.number_input("Age",1,120,25)
        gender=st.selectbox("Gender",["Male","Female","Other"])
        weight=st.number_input("Weight (kg)",20,200,60)
        height=st.number_input("Height (cm)",100,220,170)

    with col2:
        st.markdown("### 🏥 Medical Details")
        diseases=st.multiselect("Existing Conditions",
            ["Diabetes","Heart Disease","BP","Asthma","Thyroid","None"])
        allergies=st.text_input("Allergies")
        meds=st.text_input("Current Medications")
        blood=st.selectbox("Blood Group",["A+","A-","B+","B-","O+","O-","AB+","AB-"])

    if st.button("Save Profile"):
        st.success("Profile saved successfully")
        st.markdown(f"""
        **Saved Details**  
        Name: {name}  
        Age: {age}  
        Gender: {gender}  
        Conditions: {', '.join(diseases) if diseases else 'None'}
        """)

    st.markdown("---")
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
            meter=st.progress(0)
            for i in range(int(prob)):
                meter.progress(i+1)
                time.sleep(0.01)
            st.markdown(f"### Risk Probability: {prob:.2f}%")

            if prob<30:
                st.success("Low Risk")
            elif prob<70:
                st.warning("Moderate Risk")
            else:
                st.error("High Risk")


# ---------------- HEART MODULE ----------------
def heart():
    st.markdown("## Heart Disease Prediction")

    st.markdown("### Enter Patient Data")

    col1,col2,col3 = st.columns(3)

    with col1:
        age = st.number_input("Age",20,100,40)
        sex = st.selectbox("Gender",["Female","Male"])
        cp = st.selectbox("Chest Pain Type",[0,1,2,3])

    with col2:
        chol = st.number_input("Cholesterol",100,400,200)
        maxhr = st.number_input("Max Heart Rate",60,220,150)
        oldpeak = st.number_input("ST Depression",0.0,6.0,1.0)

    with col3:
        fasting = st.selectbox("Fasting Sugar >120",[0,1])
        angina = st.selectbox("Exercise Induced Angina",[0,1])
        vessels = st.selectbox("Major Vessels",[0,1,2,3])

    sex_val = 1 if sex=="Male" else 0

    if st.button("Analyze Heart Risk"):
        if heart_model is None:
            st.error("Model not loaded")
        else:
            data=np.array([[age,sex_val,cp,120,chol,fasting,0,maxhr,angina,oldpeak,vessels,0,1]])
            prob=heart_model.predict_proba(data)[0][1]*100

            st.progress(int(prob))
            meter=st.progress(0)
            for i in range(int(prob)):
                meter.progress(i+1)
                time.sleep(0.01)
            st.markdown(f"### Risk Probability: {prob:.2f}%")

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

    if page=="🏠 Dashboard": dashboard()
    elif page=="🧪 Diabetes Prediction": diabetes()
    elif page=="❤️ Heart Prediction": heart()
    elif page=="💡 Health Tips": tips()
    elif page=="🚪 Logout": logout()
