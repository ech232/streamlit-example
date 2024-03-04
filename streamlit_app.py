import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# Load your data
data = pd.read_csv('test.csv')

# Add a new column for line width, default to 5
data['Line_Width'] = 5

# Identify the route(s) with the highest Q-Value
max_q_value = data['Q-Values'].max()
# Increase line width for the best route(s)
data.loc[data['Q-Values'] == max_q_value, 'Line_Width'] = 10

# Add a color column, default to red lines
data['Line_Color'] = "[200, 30, 0, 160]"  # Red
# Change color for the best route(s) to green
data.loc[data['Q-Values'] == max_q_value, 'Line_Color'] = "[0, 255, 0, 160]"  # Green

# Streamlit app starts here
st.title('Optimal Driver Routing Plans in Boston')

# Map plotting with pydeck
layer = pdk.Layer(
    "LineLayer",
    data,
    get_source_position=["Start_Longitude", "Start_Latitude"],
    get_target_position=["End_Longitude", "End_Latitude"],
    get_color="Line_Color",  # Use the Line_Color column
    get_width="Line_Width",  # Use the Line_Width column
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

# Create a dataframe for nodes
nodes = pd.concat([
    data[['Start', 'Start_Latitude', 'Start_Longitude']],
    data[['End', 'End_Latitude', 'End_Longitude']].rename(columns={'End': 'Start', 'End_Latitude': 'Start_Latitude', 'End_Longitude': 'Start_Longitude'})
]).drop_duplicates().reset_index(drop=True)

node_layer = pdk.Layer(
    "ScatterplotLayer",
    nodes,
    get_position=["Start_Longitude", "Start_Latitude"],
    get_color="[0, 0, 255, 160]",  # Blue
    get_radius=100,  # Adjust size of the dot
    pickable=True,
)

# Add a tooltip for nodes
tooltip={"html": "<b>Location:</b> {Start}"}

# Render the map with the routes
st.pydeck_chart(pdk.Deck(
    layers=[layer, node_layer],
    initial_view_state=view_state,
    tooltip=tooltip
))
