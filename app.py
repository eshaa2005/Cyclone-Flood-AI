import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# Configuration & UI Styling
# -----------------------------
st.set_page_config(page_title="TechNova | Cyclone Flood AI", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div.stButton > button {
        width: 100%;
        height: 65px;
        font-size: 22px;
        font-weight: bold;
        background-color: #1E3A8A;
        color: white;
        border-radius: 12px;
        border: none;
    }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🌪 Cyclone-Driven Flood Risk Prediction System")
st.markdown("### **Team TechNova** | AI-Powered Disaster Preparedness Interface")

# -----------------------------
# Regional Data & Emergency Directory
# -----------------------------
region_data = {
    "Odisha": {
        "coords": (20.27, 85.84), 
        "helpline": "1078 / 0674-2534177", 
        "note": "Coastal districts like Balasore and Jagatsinghpur are highly prone to surges due to a shallow continental shelf."
    },
    "West Bengal": {
        "coords": (22.57, 88.36), 
        "helpline": "1070 / 033-22143526", 
        "note": "Low-lying deltaic terrain and the Sundarbans face severe inundation from cyclonic surges."
    },
    "Andhra Pradesh": {
        "coords": (17.68, 83.21), 
        "helpline": "1070 / 1800-425-0101", 
        "note": "A long, exposed coastline means districts like Nellore face high risk from Bay of Bengal cyclones."
    },
    "Tamil Nadu": {
        "coords": (13.08, 80.27), 
        "helpline": "1070 / 1077", 
        "note": "Northern coastal districts are significantly more vulnerable to surges during the NE monsoon."
    },
    "Assam (Northeast)": {
        "coords": (26.14, 91.73), 
        "helpline": "1070 / 1079", 
        "note": "The Brahmaputra valley faces annual floods due to intense monsoonal rainfall and river sediment."
    },
    "Meghalaya (Northeast)": {
        "coords": (25.57, 91.89), 
        "helpline": "1070 / 1077", 
        "note": "Steep gradients and narrow valleys lead to rapid rainwater accumulation and flash floods."
    },
    "Arunachal Pradesh": {
        "coords": (28.21, 94.72), 
        "helpline": "1070 / 1077", 
        "note": "Hilly terrain is susceptible to landslides and cloudburst-induced floods during peak monsoon."
    }
}


# Sidebar

with st.sidebar:
    st.header("📍 Study Area Coverage")
    region = st.selectbox("Select Region", list(region_data.keys()))
    
    st.info(f"**Vulnerability Profile:** {region_data[region]['note']}")
    
    st.header("📞 National Directory")
    st.write("🚑 Ambulance: **108 / 102**")
    st.write("🚒 Universal Emergency Number: **112**")
    st.write("🆘 NDRF Helpline: **011-24363260**")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🗺️ Target Location")
    selected_lat, selected_lon = region_data[region]["coords"]
    
    latitude = st.number_input("Latitude", value=selected_lat, format="%.4f")
    longitude = st.number_input("Longitude", value=selected_lon, format="%.4f")

    st.map(pd.DataFrame({"lat": [latitude], "lon": [longitude]}))

with col2:
    st.subheader("📍Meteorological Parameters")
    wind_speed = st.slider("Wind Speed (km/h)", 0, 250, 110)
    pressure = st.slider("Atmospheric Pressure (hPa)", 900, 1050, 990)
    # 5-day rainfall to reflect time-series analysis
    rainfall = st.slider("5-Day Cumulative Rainfall (mm)", 0, 700, 300)
    humidity = st.slider("Humidity (%)", 0, 100, 80)


st.markdown("---")
if st.button("🚨 ANALYZE FLOOD RISK"):
    rain_weight = 0.65 if "Northeast" in region or region == "Arunachal Pradesh" else 0.55
    
    risk_score = (
        rainfall * rain_weight +
        wind_speed * 0.20 +
        (1013 - pressure) * 0.15 +
        humidity * 0.10
    )

    probability = min(max(risk_score / 3.5, 0), 100)

    # Result Display
    st.subheader(f"🌊 Estimated Flood Risk Probability: {probability:.2f}%")
    st.progress(int(probability))

    # --- Precautionary Actions based on Risk Level ---
    st.markdown("### 📋 Recommended Precautionary Actions")
    
    if probability > 70:
        st.error("🔴 **CRITICAL RISK - HIGH VULNERABILITY**")
        st.markdown("""
            - **Evacuation:** Immediate movement to designated high-ground shelters or RCC buildings.
            - **Power Safety:** Switch off all electrical mains and gas connections before water enters the premises.
            - **Emergency Kit:** Carry your 'Go-Bag' with 72-hour dry rations, medications, and waterproofed documents.
            - **Communication:** Continuously monitor local radio/TV for NDMA/IMD evacuation orders.
        """)
        st.error("🔴 **CRITICAL ALERT: IMMEDIATE ACTION REQUIRED**")
        st.markdown(f"""
            <div class="emergency-card">
                <h3 style="color: #c53030; margin-top: 0;">🆘 {region.upper()} SHELTER & HELPLINE</h3>
                <p><b>State Emergency Helpline:</b> {region_data[region]['helpline']}</p>
                <p><b>District Control Room:</b> 1077 (Toll-Free)</p>
                <p><b>Shelter Protocol:</b> Proceed to the nearest <b>Multipurpose Cyclone Shelter (MCS)</b>. In coastal areas, these are usually marked with yellow and blue signage. Contact your local BDO (Block Development Officer) for the precise site list.</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("- **Evacuation:** Leave low-lying areas immediately.\n- **Utilities:** Turn off gas and electricity.")

    elif probability > 40:
        st.warning("🟠 **MODERATE RISK - STAY ALERT**")
        st.markdown("""
            - **Resource Stockpiling:** Ensure adequate stock of drinking water (boiled/filtered) and non-perishable food.
            - **Property Protection:** Secure loose outdoor objects like tin roofs and move valuables to higher floors.
            - **Health Preparedness:** Stock up on basic first aid and specific chronic medicines for family members.
            - **Vigilance:** Watch for localized waterlogging or rising river levels (typically 24-72h after rainfall).
        """)
    else:
        st.success("🟢 **LOW RISK - MONITORING MODE**")
        st.markdown("""
            - **Regular Updates:** Track weather updates via meteorological APIs and local news.
            - **Maintenance:** Ensure household drainage systems are clear of blockages and debris.
            - **Plan Review:** Review family emergency meeting points and evacuation routes with all members.
        """)

    # -----------------------------
    # Impact Visualization
    # -----------------------------
    st.markdown("---")
    st.subheader("📉 Risk Factor Contribution Analysis")
    
    features = ["Rainfall", "Wind Speed", "Pressure", "Humidity"]
    impact_vals = [rainfall * rain_weight, wind_speed * 0.20, (1013 - pressure) * 0.15, humidity * 0.10]

    fig, ax = plt.subplots(figsize=(8, 4))
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, 4))
    ax.barh(features, impact_vals, color=colors)
    ax.set_xlabel("Impact Level on Prediction")
    ax.invert_yaxis()
    st.pyplot(fig)

st.markdown("---")
st.markdown("<center><small>Developed for SPARK 2.0 | TechNova Hackathon Prototype 2026</small></center>", unsafe_allow_html=True)


