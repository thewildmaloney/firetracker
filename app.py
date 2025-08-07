import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Map Test", layout="wide")
st.title("🧪 Minimal Map Test")

# Set your Mapbox token from secrets
pdk.settings.mapbox_api_key = st.secrets["MAPBOX_API_KEY"]

# Dummy location near Dolores, CO
test_data = pd.DataFrame({
    "lat": [37.5444],
    "lon": [-108.4878]
})

# One layer, one dot
test_layer = pdk.Layer(
    "ScatterplotLayer",
    data=test_data,
    get_position='[lon, lat]',
    get_color='[0, 200, 255, 160]',
    get_radius=500
)

# Render basic map
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(latitude=37.5444, longitude=-108.4878, zoom=10),
    layers=[test_layer]
))

st.caption("If you see a blue dot near Dolores, your Mapbox token and pydeck setup are working.")