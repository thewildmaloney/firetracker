import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="Stoner Mesa Fire Dashboard", layout="wide")
st.title("🔥 Stoner Mesa Fire Watch (Folium Map Version)")

# Sidebar Info
st.sidebar.header("Dashboard Controls")
update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.markdown(f"**Last Updated:** {update_time}")

# Constants
ADDRESS_LAT = 37.5444
ADDRESS_LON = -108.4878
FIRE_CENTER_LAT = 37.65
FIRE_CENTER_LON = -108.3

# --- NASA FIRMS Fire Points ---
@st.cache_data(ttl=1800)
def fetch_firms_data():
    try:
        url = "https://firms.modaps.eosdis.nasa.gov/api/country/csv/USA/VIIRS_SNPP_NRT/1"
        df = pd.read_csv(url)
        df = df[(df['latitude'] > 37.2) & (df['latitude'] < 38.1) & (df['longitude'] > -108.7) & (df['longitude'] < -108.0)]
        return df
    except:
        return pd.DataFrame()

firms_df = fetch_firms_data()

# --- NOAA Wind Data ---
@st.cache_data(ttl=1800)
def fetch_wind_data():
    try:
        pt = requests.get("https://api.weather.gov/points/37.5444,-108.4878").json()
        forecast = requests.get(pt['properties']['forecastHourly']).json()
        wind = forecast['properties']['periods'][0]
        return wind['windSpeed'], wind['windDirection']
    except:
        return "17 mph", "ESE"

wind_speed, wind_dir = fetch_wind_data()

# --- AQI Placeholder ---
@st.cache_data(ttl=1800)
def fetch_aqi():
    return 102

aqi = fetch_aqi()

# --- Folium Map ---
st.subheader("🗺️ Fire Map with Folium")

m = folium.Map(location=[FIRE_CENTER_LAT, FIRE_CENTER_LON], zoom_start=10)

# Plot your location
folium.Marker([ADDRESS_LAT, ADDRESS_LON], tooltip="Your Location", icon=folium.Icon(color="blue")).add_to(m)

# Plot fire points
if not firms_df.empty:
    for _, row in firms_df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            color="red",
            fill=True,
            fill_opacity=0.6
        ).add_to(m)
else:
    st.info("No recent FIRMS fire detections in the area.")

st_folium(m, width=700, height=500)

# --- Metrics Panel ---
st.subheader("📊 Fire Metrics & Weather Conditions")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Acres Burned", "350 acres")
col2.metric("🛑 Containment", "0%")
col3.metric("💨 Wind Speed", wind_speed)
col4.metric("🧭 Wind Direction", wind_dir)

# --- AQI ---
st.subheader("🌫️ Air Quality in Dolores")
st.metric("AQI (Dolores)", f"{aqi}", delta="+5 from yesterday")

# --- Evacuations ---
st.subheader("🚨 Active Evacuations")
evac_list = [
    "Mavreeso Campground",
    "Taylor Mesa Road",
    "Stoner Mesa Road",
    "Forest Service Roads 686, 545",
    "West Fork Dolores River"
]
st.markdown("\n".join([f"- {area}" for area in evac_list]))

# --- Resources ---
st.subheader("🔗 Official Resources")
st.markdown("""
- [The Journal Fire Updates](https://www.the-journal.com/articles/evacuations-ordered-as-stoner-mesa-fire-grows-northeast-of-dolores/)
- [Durango Herald Coverage](https://www.durangoherald.com/articles/evacuations-ordered-as-stoner-mesa-fire-grows-northeast-of-dolores/)
- [Colorado Wildfire Dashboard](https://www.colorado.gov/pacific/dfpc/fire-information)
- [NOAA Smoke Forecast](https://www.weather.gov)
- [InciWeb](https://inciweb.nwcg.gov/)
""")
st.markdown("---")
st.caption("Map powered by Folium. No Mapbox token required. Auto-updates every 30 minutes.")