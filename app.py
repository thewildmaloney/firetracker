# Stoner Mesa Fire Dashboard for Streamlit Cloud

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Title ---
st.set_page_config(page_title="Stoner Mesa Fire Dashboard", layout="wide")
st.title("🔥 Stoner Mesa Fire Watch")

# --- Sidebar Controls ---
st.sidebar.header("Dashboard Controls")
update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.markdown(f"**Last Updated:** {update_time}")

# --- Constants ---
ADDRESS_LAT = 37.5444
ADDRESS_LON = -108.4878  # Approximate location of 27551 HWY 145, Dolores
FIRE_CENTER_LAT = 37.65
FIRE_CENTER_LON = -108.3

# --- Map Panel ---
st.subheader("🗺️ Current Fire Map")
map_df = pd.DataFrame({
    'label': ["Your Location", "Fire Center"],
    'lat': [ADDRESS_LAT, FIRE_CENTER_LAT],
    'lon': [ADDRESS_LON, FIRE_CENTER_LON],
    'color': ["blue", "red"]
})
fig = px.scatter_mapbox(map_df,
                        lat="lat",
                        lon="lon",
                        hover_name="label",
                        color="color",
                        zoom=9,
                        height=500)
fig.update_layout(mapbox_style="open-street-map")
fig.update_traces(marker=dict(size=14))
st.plotly_chart(fig, use_container_width=True)

# --- Metrics Gauges ---
st.subheader("📊 Fire Metrics & Weather Conditions")

col1, col2, col3, col4 = st.columns(4)

# Static data for prototype
fire_acres = 350
containment = 0
wind_speed = 17  # mph
wind_dir = "ESE"

col1.metric("🔥 Acres Burned", f"{fire_acres} acres")
col2.metric("🛑 Containment", f"{containment}%")
col3.metric("💨 Wind Speed", f"{wind_speed} mph")
col4.metric("🧭 Wind Direction", wind_dir)

# --- Evacuations ---
st.subheader("🚨 Active Evacuations")
evac_list = [
    "Mavreeso Campground",
    "Taylor Mesa Road",
    "Stoner Mesa Road",
    "Forest Service Roads 686, 545",
    "West Fork Dolores River"
]
st.write("**Mandatory Evacuations:**")
st.markdown("\n".join([f"- {area}" for area in evac_list]))

# --- Air Quality Index ---
st.subheader("🌫️ Air Quality in Dolores")

aqi = 102  # Moderate to Unhealthy for Sensitive Groups (example only)
st.metric("AQI (Dolores)", f"{aqi}", delta="+5 from yesterday")

# --- External Links ---
st.subheader("🔗 Official Resources")
st.markdown("""
- [The Journal Fire Updates](https://www.the-journal.com/articles/evacuations-ordered-as-stoner-mesa-fire-grows-northeast-of-dolores/)
- [Durango Herald Coverage](https://www.durangoherald.com/articles/evacuations-ordered-as-stoner-mesa-fire-grows-northeast-of-dolores/)
- [Colorado Wildfire Dashboard](https://www.colorado.gov/pacific/dfpc/fire-information)
- [NOAA Smoke Forecast](https://www.weather.gov)
- [InciWeb](https://inciweb.nwcg.gov/)
""")

st.markdown("---")
st.caption("This dashboard auto-updates every 30 minutes. Built by GPT-4o + Streamlit.")
