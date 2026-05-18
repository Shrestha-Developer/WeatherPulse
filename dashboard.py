import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

API_KEY = os.getenv("SM_weather") or os.getenv("OPENWEATHER_API_KEY") or os.getenv("API_KEY")

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* Remove top gap */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* Main App Background */
.stApp {
    background: linear-gradient(to right, #000814, #001d3d);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1f2937;
}

/* Input box */
.stTextInput input {
    background-color: #0f172a;
    color: white;
    border-radius: 10px;
    border: 1px solid #334155;
}

/* Button */
.stButton button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid #ef4444;
    background: #1e293b;
    color: white;
    font-weight: bold;
    padding: 10px;
}

.stButton button:hover {
    background: #334155;
    border: 1px solid #f87171;
}

/* KPI CARDS */
.kpi-card {
    padding: 25px;
    border-radius: 18px;
    color: white;
    text-align: center;
    font-weight: bold;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}

/* Card Colors */
.temp {
    background: linear-gradient(135deg, #36d1dc, #5b86e5);
}

.humidity {
    background: linear-gradient(135deg, #11998e, #38ef7d);
}

.wind {
    background: linear-gradient(135deg, #ff8008, #ffc837);
}

.weather {
    background: linear-gradient(135deg, #8e2de2, #ff00ff);
}

/* Alerts */
.alert-box {
    background: rgba(255, 255, 0, 0.25);
    padding: 15px;
    border-radius: 12px;
    color: #fff176;
    font-weight: bold;
}

.safe-box {
    background: rgba(0, 255, 100, 0.25);
    padding: 15px;
    border-radius: 12px;
    color: #b9fbc0;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🔍 Search Weather")

    city_name = st.text_input(
        "Enter City Name",
        "Chennai"
    )

    get_weather = st.button("Get Weather")

# =========================
# TITLE
# =========================
st.markdown("""
<h1 style='font-size:48px; margin-bottom:0;'>
🌤️ WEATHERPULSE
</h1>

<p style='color:#cbd5e1; margin-top:0;'>
Real-Time Weather Monitoring and Alert System
</p>
""", unsafe_allow_html=True)

# =========================
# WEATHER FETCH
# =========================
if get_weather:

    # CHECK API KEY
    if not API_KEY:
        st.error("API Key not found. Check your .env file.")
        st.stop()

    # API URL
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    )

    # API REQUEST
    response = requests.get(url)
    data = response.json()

    # ERROR HANDLING
    if response.status_code != 200:
        st.error(f"Error: {data.get('message', 'API issue')}")
        st.stop()

    # =========================
    # WEATHER DATA
    # =========================
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"].title()
    wind_speed = data["wind"]["speed"]

    # =========================
    # ALERTS
    # =========================
    alerts = []

    if temp > 35:
        alerts.append("🔥 High Temperature Alert")

    if humidity > 85:
        alerts.append("⚠️ High Humidity Alert")

    if wind_speed > 15:
        alerts.append("🌪️ High Wind Speed Alert")

    # =========================
    # LIVE REPORT TITLE
    # =========================
    st.markdown(f"""
    <h2 style='margin-top:25px;'>
    📍 Live Weather Report - {city_name.title()}
    </h2>
    """, unsafe_allow_html=True)

    # =========================
    # KPI CARDS
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card temp">
            <h3>🌡️ Temperature</h3>
            <h1>{temp} °C</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card humidity">
            <h3>💧 Humidity</h3>
            <h1>{humidity} %</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card wind">
            <h3>🍃 Wind Speed</h3>
            <h1>{wind_speed} m/s</h1>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card weather">
            <h3>☁️ Weather</h3>
            <h1>{weather}</h1>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # ALERT SECTION
    # =========================
    st.markdown("## 🚨 Weather Alerts")

    if alerts:
        for alert in alerts:
            st.markdown(
                f"<div class='alert-box'>{alert}</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div class='safe-box'>✅ No Weather Alerts</div>",
            unsafe_allow_html=True
        )

    # =========================
    # CHART SECTION
    # =========================
    st.markdown("## 📊 Weather Analytics")

    weather_df = pd.DataFrame({
        "Parameters": [
            "Temperature",
            "Humidity",
            "Wind Speed"
        ],
        "Values": [
            temp,
            humidity,
            wind_speed
        ]
    })

    # CHART SIZE
    fig, ax = plt.subplots(figsize=(7, 3.5))

    # BAR CHART
    bars = ax.bar(
        weather_df["Parameters"],
        weather_df["Values"],
        color=[
            "#38bdf8",
            "#4ade80",
            "#fb923c"
        ],
        width=0.5
    )

    # CHART THEME
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    ax.tick_params(
        colors='white',
        labelsize=14
    )

    for spine in ax.spines.values():
        spine.set_color('#334155')

    # TITLE
    ax.set_title(
        f"{city_name.title()} Weather Data",
        color='white',
        fontsize=24,
        fontweight='bold',
        loc='left',
        pad=20
    )

    ax.set_ylabel(
        "Values",
        color='white',
        fontsize=14
    )

    ax.grid(
        axis='y',
        linestyle='--',
        alpha=0.3,
        color='white'
    )

    # LABELS
    for bar in bars:
        yval = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width()/2,
            yval + 1,
            round(yval, 1),
            ha='center',
            color='white',
            fontsize=12,
            fontweight='bold'
        )

    # DISPLAY CHART
    chart_col1, chart_col2 = st.columns([3,1])

    with chart_col1:
        st.pyplot(fig, use_container_width=True)

    # =========================
    # SAVE CSV
    # =========================
    os.makedirs(
        "outputs",
        exist_ok=True
    )

    report_df = pd.DataFrame({
        "City": [city_name.title()],
        "Temperature": [temp],
        "Humidity": [humidity],
        "Weather": [weather],
        "Wind Speed": [wind_speed],
        "Alerts": [
            ", ".join(alerts)
            if alerts else "No Alerts"
        ]
    })

    csv_path = (
        f"outputs/"
        f"{city_name}_weather_report.csv"
    )

    report_df.to_csv(
        csv_path,
        index=False
    )

    # DOWNLOAD BUTTON
    with open(csv_path, "rb") as file:

        st.download_button(
            label="⬇ Download Weather Report CSV",
            data=file,
            file_name=f"{city_name}_weather_report.csv",
            mime="text/csv"
        )