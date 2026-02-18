import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="HealthGuard Pro", page_icon="🩺", layout="wide")

# Load models
diabetes_model = pickle.load(open("model.pkl", "rb"))
heart_model = pickle.load(open("heart_model.pkl", "rb"))

# Sidebar
st.sidebar.title("🩺 HealthGuard Pro")
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
disease = st.sidebar.radio("Choose Assessment", ["Diabetes", "Heart Disease"])

if theme == "Dark":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

st.title("🩺 AI Health Risk Prediction Dashboard")
st.markdown("Real-time multi-disease prediction system powered by Machine Learning")

# ================= DIABETES =================
if disease == "Diabetes":

    st.subheader("Diabetes Risk Assessment")

    col1, col2 = st.columns(2)

    with col1:
        preg = st.number_input("Pregnancies", min_value=0)
        glucose = st.slider("Glucose Level", 0, 200, 100)
        bp = st.slider("Blood Pressure", 0, 150, 70)
        insulin = st.slider("Insulin", 0, 900, 80)

    with col2:
        height = st.number_input("Height (meters)", min_value=1.0, max_value=2.5)
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0)
        age = st.slider("Age", 1, 100, 25)
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0)

    bmi = weight / (height ** 2)
    st.write(f"### Calculated BMI: {bmi:.2f}")

    if st.button("Analyze Diabetes Risk"):

        input_data = np.array([[preg, glucose, bp, 20, insulin, bmi, dpf, age]])
        probability = diabetes_model.predict_proba(input_data)[0][1] * 100

        st.progress(int(probability))
        st.write(f"### Risk Probability: {probability:.2f}%")

        if probability < 30:
            st.success("🟢 Low Risk")
        elif probability < 70:
            st.warning("🟡 Moderate Risk")
        else:
            st.error("🔴 High Risk - Consult Doctor")

        fig, ax = plt.subplots()
        ax.bar(["Safe", "Risk"], [100 - probability, probability])
        ax.set_ylabel("Percentage")
        st.pyplot(fig)

# ================= HEART =================
elif disease == "Heart Disease":

    st.subheader("Heart Disease Risk Assessment")

    age = st.slider("Age", 20, 100, 40)
    cholesterol = st.slider("Cholesterol", 100, 400, 200)
    max_hr = st.slider("Maximum Heart Rate", 60, 220, 150)
    oldpeak = st.slider("ST Depression (Oldpeak)", 0.0, 6.0, 1.0)

    # Default values for remaining features (based on common heart dataset)
    input_data = np.array([[age, 1, 0, 120, cholesterol, 0, 0, max_hr, 0, oldpeak, 0, 0, 1]])

    if st.button("Analyze Heart Risk"):

        probability = heart_model.predict_proba(input_data)[0][1] * 100

        st.progress(int(probability))
        st.write(f"### Heart Disease Risk: {probability:.2f}%")

        if probability < 30:
            st.success("🟢 Low Risk")
        elif probability < 70:
            st.warning("🟡 Moderate Risk")
        else:
            st.error("🔴 High Risk - Seek Medical Advice")

        fig, ax = plt.subplots()
        ax.pie([probability, 100 - probability],
               labels=["Risk", "Safe"],
               autopct="%1.1f%%")
        st.pyplot(fig)
