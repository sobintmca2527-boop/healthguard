import streamlit as st
import pickle
import numpy as np

# Page settings
st.set_page_config(page_title="HealthGuard", page_icon="🩺", layout="centered")

# Custom styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.title("🩺 HealthGuard")
st.subheader("AI-Based Diabetes Risk Prediction")

st.write("Fill in your health details below to check your risk level.")

# Input layout in 2 columns
col1, col2 = st.columns(2)

with col1:
    preg = st.number_input("Pregnancies", min_value=0, max_value=20)
    glucose = st.number_input("Glucose Level", min_value=0)
    bp = st.number_input("Blood Pressure", min_value=0)
    skin = st.number_input("Skin Thickness", min_value=0)

with col2:
    insulin = st.number_input("Insulin", min_value=0)
    bmi = st.number_input("BMI", min_value=0.0)
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0)
    age = st.number_input("Age", min_value=1, max_value=120)

if st.button("Predict Risk"):
    data = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
    probability = model.predict_proba(data)[0][1] * 100

    st.subheader(f"Risk Probability: {probability:.2f}%")

    if probability < 30:
        st.success("🟢 Low Risk")
        st.info("Maintain healthy diet and regular exercise.")
    elif probability < 70:
        st.warning("🟡 Moderate Risk")
        st.info("Consider lifestyle changes and regular checkups.")
    else:
        st.error("🔴 High Risk")
        st.info("Please consult a medical professional immediately.")
