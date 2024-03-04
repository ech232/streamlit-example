import streamlit as st
import pandas as pd
import pydeck as pdk

# Assume final_qtables is the DataFrame from the join operation
final_qtables = pd.read_csv('data.csv') # Change this file name to whatever final table is

# Find the maximum Q-value
max_q_value = final_qtables['Q'].max()

# Create a new column for color, default to a specific color for all
default_color = [0, 255, 0, 160]  # Green lines
highlight_color = [255, 0, 0, 160]  # Red lines for the best Q-value
final_qtables['color'] = final_qtables.apply(
    lambda row: highlight_color if row['Q'] == max_q_value else default_color, axis=1
)

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

# Map plotting with pydeck
line_layer = pdk.Layer(
    "LineLayer",
    filtered_data,
    get_source_position=["Start_Longitude", "Start_Latitude"],
    get_target_position=["End_Longitude", "End_Latitude"],
    get_color="color",  # Use the color column for line color
    get_width=4,  # Uniform line weight
    pickable=True,
    auto_highlight=True,
)

# Set the view for Boston
view_state = pdk.ViewState(
    latitude=filtered_data["Start_Latitude"].mean(),  # Center the view on the data
    longitude=filtered_data["Start_Longitude"].mean(),
    zoom=11,
    pitch=0,
)

# Render the map with the routes
st.pydeck_chart(pdk.Deck(
    layers=[line_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v9",  # Light mode map
    tooltip={
        "html": "<b>Source:</b> {Source}<br>"
                "<b>Destination:</b> {Destination}<br>"
                "<b>Q-Value:</b> {Q}"
    }
))
