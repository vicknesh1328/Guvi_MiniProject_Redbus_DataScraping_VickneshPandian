# %%
import mysql.connector
import pandas as pd
import streamlit as st

def display_data_from_db():
    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(
        host="127.0.0.1",      
        user="root",        
        password="vicky",
        database="test"   
    )
    cursor = conn.cursor()

    # Execute SQL query to retrieve data
    cursor.execute("SELECT * FROM RedBus_DataScraping_09")
    rows = cursor.fetchall()

    # Create a DataFrame from the database rows
    df = pd.DataFrame(rows, columns=[
        'ID', 'Orgin_Place', 'Destination_Place', 'Bus_Name', 
        'Onboard_Time', 'Travel_Time', 'Arrival_Time', 'Rating', 
        'Price', 'Seat_Avail'
    ])

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Handle missing values by filling them with defaults
    df.fillna({
        'Orgin_Place': 'Unknown',
        'Destination_Place': 'Unknown',
        'Price': 0,
        'Rating': 0,
        'Seat_Avail': 'No Info',
        'Bus_Name': 'Unknown'
    }, inplace=True)

    # --- Streamlit App: Add Filters ---
    st.title("RED BUS DATA SCRAPING GUVI MINI PROJECT")

    # Add sidebar for navigation
    st.sidebar.title("Main Menu")
    st.sidebar.button("Select the Bus")

    # Route selection (dropdown)
    route_options = df['Orgin_Place'] + " to " + df['Destination_Place']
    selected_route = st.selectbox("Select the Route", route_options.unique())

    # Seat Availability filter (dropdown)
    seat_options = df['Seat_Avail'].unique()
    selected_seat_avail = st.selectbox("Select Seat Availability", seat_options)

    # Ratings filter (dropdown)
    rating_filter = st.selectbox("Select the Ratings", ["3 to 4", "4 to 5"])

    # Starting time filter (slider) - using Onboard Time
    onboard_time_filter = st.slider("Onboard Time", 0, 24, (22, 23), format="%d:00")

    # Bus fare range (dropdown)
    bus_fare_filter = st.selectbox("Bus Fare Range", ["less than 500", "500 to 1000", "others"])

    # --- Apply Filters to the DataFrame ---
    
    # Filter by selected route
    start, reach = selected_route.split(" to ")
    filtered_df = df[(df['Orgin_Place'] == start) & (df['Destination_Place'] == reach)]

    # Filter by seat availability
    filtered_df = filtered_df[filtered_df['Seat_Avail'] == selected_seat_avail]

    # Filter by ratings
    if rating_filter == "3 to 4":
        filtered_df = filtered_df[(filtered_df['Rating'].astype(float) >= 3) & (filtered_df['Rating'].astype(float) <= 4)]
    elif rating_filter == "4 to 5":
        filtered_df = filtered_df[(filtered_df['Rating'].astype(float) >= 4) & (filtered_df['Rating'].astype(float) <= 5)]

    # Filter by bus fare range
    if bus_fare_filter == "less than 500":
        filtered_df = filtered_df[filtered_df['Price'].astype(float) < 500]
    elif bus_fare_filter == "500 to 1000":
        filtered_df = filtered_df[(filtered_df['Price'].astype(float) >= 500) & (filtered_df['Price'].astype(float) <= 1000)]

    
    st.dataframe(filtered_df)

# Streamlit App code - run this in Streamlit
if __name__ == "__main__":
    display_data_from_db()


# %%

