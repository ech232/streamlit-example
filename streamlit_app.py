import streamlit as st
import pandas as pd
import pydeck as pdk

# Load your data
data = pd.read_csv('test.csv')

# Streamlit app starts here
st.title('Optimal Driver Routing Plans in Boston')

# Map plotting with pydeck
layer = pdk.Layer(
    "LineLayer",  # Use LineLayer to draw lines between start and end points
    data,
    get_source_position=["Start_Longitude", "Start_Latitude"],
    get_target_position=["End_Longitude", "End_Latitude"],
    get_color="[200, 30, 0, 160]",  # RGBA color of the lines
    get_width=10,
    pickable=True,
    auto_highlight=True,
)

# Set the view for Boston
view_state = pdk.ViewState(
    latitude=data["Start_Latitude"].mean(),  # Center the view on the data
    longitude=data["Start_Longitude"].mean(),
    zoom=11,
    pitch=0,
)

# Render the map with the routes
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    # Tooltip to display route and reward information on hover
    tooltip={"html": "<b>Start:</b> {Start}<br><b>End:</b> {End}<br><b>Q-Value:</b> {Q-Values}"}
))
