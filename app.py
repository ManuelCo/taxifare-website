import streamlit as st
import datetime
import requests
import pandas as pd

url = 'https://taxifare.lewagon.ai/predict'

st.title("Hey Bro, let's pickup your next F ride!")

st.title("Date and Time Picker")
date = st.date_input("Select date", value=datetime.date(2019, 7, 6))
time = st.time_input("Select time", value=datetime.time(8, 45))
combined_datetime = datetime.datetime.combine(date, time)
st.write("Selected Date and Time:", combined_datetime)

st.title("Ride Details")

pickup_longitude = st.number_input("Enter pickup longitude", value=None, placeholder="Type longitude...")
pickup_latitude = st.number_input("Enter pickup latitude", value=None, placeholder="Type latitude...")
dropoff_longitude = st.number_input("Enter dropoff longitude", value=None, placeholder="Type longitude...")
dropoff_latitude = st.number_input("Enter dropoff latitude", value=None, placeholder="Type latitude...")

Number_of_passentger = st.select_slider(
    "Enter passenger count",
    options=["1", "2", "3", "4", "5", "6", "7"])
st.write("You selected", Number_of_passentger, "passengers")

data = {
    "pickup_datetime": combined_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": int(Number_of_passentger)
}

st.json(data)

map_data = pd.DataFrame([
    {"lat": pickup_latitude, "lon": pickup_longitude, "type": "Pickup"},
    {"lat": dropoff_latitude, "lon": dropoff_longitude, "type": "Dropoff"}
])

# Display the map with pickup and dropoff locations
st.subheader("Ride Map")
st.map(map_data)

# Button to trigger the API call
if st.button("Get Prediction"):
    # Send a GET request to the API
    response = requests.get(url, params=data)

    # Check if the request was successful
    if response.status_code == 200:
        prediction = response.json()
        st.success(f"Prediction: {prediction}")
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
