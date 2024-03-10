import streamlit as st
    import pandas as pd
    import pydeck as pdk

    # Load the data
    final_qtables = pd.read_csv('data/data.csv')  # Make sure this is the correct path to your data file

    # Streamlit app starts here
    st.title('Optimal Driver Routing Plans in Boston')

    # Filter data based on user input
    filtered_data = final_qtables[(final_qtables['hour'] == chosen_hour) & 
                                  (final_qtables['day'] == driver_day) & 
                                  (final_qtables['weather'] == driver_short_summary) &
                                  (final_qtables['Source'] == driver_source)].copy()

    # Function to assign color based on Q-value
    def assign_color(row, max_q_value):
        if row['Q'] == max_q_value:
            return [0, 255, 0, 160]  # Green for the highest Q-value
        else:
            return [255, 0, 0, 160]  # Red for other routes

    # Find the maximum Q-value within the filtered data
    max_q_value = filtered_data['Q'].max()

    # Apply the function to assign colors
    filtered_data['color'] = filtered_data.apply(assign_color, axis=1, max_q_value=max_q_value)

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
        latitude=filtered_data["Start_Latitude"].mean(),
        longitude=filtered_data["Start_Longitude"].mean(),
        zoom=11,
        pitch=0,
    )

    # Render the map with the routes
    st.pydeck_chart(pdk.Deck(
        layers=[line_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v9",
        tooltip={
            "html": "<b>Source:</b> {Source}<br>"
                    "<b>Destination:</b> {Destination}<br>"
                    "<b>Q-Value:</b> {Q}"
    }
))

