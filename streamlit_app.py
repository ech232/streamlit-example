import streamlit as st
import pandas as pd
import pydeck as pdk

# Assume final_qtables is the DataFrame from the join operation
final_qtables = pd.read_csv('data.csv') # change this file name to whatever final table is

# Streamlit app starts here
st.title('Optimal Driver Routing Plans in Boston')

# User input for filtering
hour = st.selectbox('Choose hour', sorted(final_qtables['hour'].unique()), index=0)
day = st.selectbox('Choose day', sorted(final_qtables['day'].unique()), index=0)
weather = st.selectbox('Choose weather', sorted(final_qtables['weather'].unique()), index=0)

# Filter data based on user input
filtered_data = final_qtables[(final_qtables['hour'] == hour) & 
                              (final_qtables['day'] == day) & 
                              (final_qtables['weather'] == weather)]

# Normalize the Q values
final_qtables['Q'] /= final_qtables['Q'].max()
final_qtables['Q'] *= 10 

# Plot lines for routes
layer = pdk.Layer(
    "LineLayer",
    filtered_data,
    get_source_position=["Start_Longitude", "Start_Latitude"],
    get_target_position=["End_Longitude", "End_Latitude"],
    get_color="[20, 255, 20, 160]",  # Green lines
    get_width="Q",  # Use the Q column for line thickness
    pickable=True,
    auto_highlight=True,
)

# Plot "nodes" for each location
locations_data = pd.concat([
    filtered_data[['Source', 'Start_Latitude', 'Start_Longitude']],
    filtered_data[['Destination', 'End_Latitude', 'End_Longitude']].rename(columns={
        'Destination': 'Source', 'End_Latitude': 'Start_Latitude', 'End_Longitude': 'Start_Longitude'
    })
]).drop_duplicates().reset_index(drop=True)

# Set the view for Boston
view_state = pdk.ViewState(
    latitude=filtered_data["Start_Latitude"].mean(),  # Center the view on the data
    longitude=filtered_data["Start_Longitude"].mean(),
    zoom=11,
    pitch=0,
)

# Render the map with the routes and location dots
st.pydeck_chart(pdk.Deck(
    layers=[line_layer, location_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v9",  # Light mode map
    tooltip={
        "html": "<b>Source:</b> {Source}<br>"
                "<b>Destination:</b> {Destination}<br>"
                "<b>Q-Value:</b> {Q}"
    }
))
