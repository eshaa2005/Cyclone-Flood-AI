import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cyclone Flood AI", layout="wide")

st.title("🌪 Cyclone-Driven Flood Risk Prediction System")
st.markdown("AI-powered early warning system for cyclone-induced flooding.")

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Location")
    latitude = st.number_input("Latitude", value=20.0)
    longitude = st.number_input("Longitude", value=75.0)

    st.map(pd.DataFrame({
        "lat": [latitude],
        "lon": [longitude]
    }))

with col2:
    st.subheader("🌦 Weather Parameters")

    wind_speed = st.slider("Wind Speed (km/h)", 0, 250, 80)
    pressure = st.slider("Pressure (hPa)", 900, 1050, 1000)
    rainfall = st.slider("3-Day Rainfall (mm)", 0, 500, 150)
    humidity = st.slider("Humidity (%)", 0, 100, 75)

# -----------------------------
# Centered Big Predict Button
# -----------------------------
st.markdown(
    """
    <style>
    div.stButton > button {
        width: 100%;
        height: 70px;
        font-size: 22px;
        font-weight: bold;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col_center1, col_center2, col_center3 = st.columns([1, 2, 1])

with col_center2:
    predict_clicked = st.button("🚨 PREDICT FLOOD RISK")

# -----------------------------
# Prediction Logic
# -----------------------------
if predict_clicked:

    risk_score = (
        rainfall * 0.5 +
        wind_speed * 0.3 +
        (1010 - pressure) * 0.1 +
        humidity * 0.1
    )

    probability = min(max(risk_score / 2, 0), 100)

    st.subheader(f"🌊 Flood Risk Probability: {probability:.2f}%")
    st.progress(int(probability))

    if probability > 70:
        st.error("🔴 HIGH FLOOD RISK — Immediate Preparedness Required!")
    elif probability > 40:
        st.warning("🟠 MODERATE FLOOD RISK — Stay Alert.")
    else:
        st.success("🟢 LOW FLOOD RISK — Conditions Stable.")

    # -----------------------------
    # Smaller Feature Chart
    # -----------------------------
    st.markdown("---")
    st.subheader("📊 Risk Factor Contribution")

    features = ["Rainfall", "Wind Speed", "Pressure", "Humidity"]
    values = [
        rainfall * 0.5,
        wind_speed * 0.3,
        (1010 - pressure) * 0.1,
        humidity * 0.1
    ]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.barh(features, values)
    ax.set_xlabel("Impact Level")
    ax.invert_yaxis()
    ax.tick_params(labelsize=8)

    st.pyplot(fig)

# -----------------------------
# Footer Section
# -----------------------------
st.markdown("---")
st.markdown(
    "<center><small>Developed for Disaster Risk Management | Hackathon Prototype 2026</small></center>",
    unsafe_allow_html=True
)

