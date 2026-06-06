import streamlit as st
import hopsworks
import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt

# Connect to Hopsworks
project = hopsworks.login(api_key_value=st.secrets["HOPSWORKS_API_KEY"])
mr = project.get_model_registry()
model = joblib.load(mr.get_model("aqi_model", version=1).download() + "/aqi_model.pkl")

st.title("Air Quality Index Predictor")

# Real-time Prediction Logic
# [Insert logic to pull latest features here]
prediction = model.predict([[12, 1, 6, 22, 50]])[0] 

st.metric("Predicted AQI", round(prediction, 2))

# Hazardous Alerts
if prediction > 150:
    st.error("⚠️ HAZARDOUS: Take precautions!")
elif prediction > 100:
    st.warning("Unhealthy levels.")
else:
    st.success("Air Quality is Good.")