import pydeck as pdk
import streamlit as st
import matplotlib.pyplot as plt
from utils import getNWS

# HTML and JavaScript to get user location
get_location_html = """
<script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    // Set the hidden inputs and submit the form
                    document.getElementById("latitude").value = latitude;
                    document.getElementById("longitude").value = longitude;
                    document.getElementById("locationForm").submit();
                },
                (error) => {
                    console.error("Error getting location:", error);
                    alert("Unable to fetch location. Please allow location access.");
                }
            );
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    }
    window.onload = getLocation;
</script>
<form id="locationForm" method="post">
    <input type="hidden" id="latitude" name="latitude">
    <input type="hidden" id="longitude" name="longitude">
</form>
"""

# Display the HTML
st.components.v1.html(get_location_html, height=0)

# Capture the posted data
query_params = st.query_params
# latitude = query_params.get("latitude")
# longitude = query_params.get("longitude")
longitude = 43.7328149
latitude = -111.0904983

if latitude and longitude:
    st.success(f"Viewing weather data for Coordinates: Latitude {latitude}, Longitude {longitude}")
    # You can now use the latitude and longitude in your code
else:
    st.info("Waiting for location...")



geoJSON, dewPoint = getNWS(longitude, latitude)



geojson_layer = pdk.Layer(
    "GeoJsonLayer",
    geoJSON,  # Pass the GeoJSON directly
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color=[255, 0, 0, 100],  # RGBA for fill
    get_line_color=[0, 0, 0, 200],   # RGBA for line
)

# Define the viewport for the map
view_state = pdk.ViewState(
    # longitude= geoJSON["geometry"]["coordinates"][0],  # Adjust based on your data
    # latitude= geoJSON["geometry"]["coordinates"][1],
    latitude = 43.7328149,
    longitude = -111.0904983,
    zoom=10,
    pitch=0,
) 

# Render the map
st.title("Local Area Map")
st.pydeck_chart(pdk.Deck(layers=[geojson_layer], initial_view_state=view_state))

st.title("Dewpoint Forecast")

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(dewPoint['DateTime'], dewPoint['Dewpoint (°F)'], marker='o', linestyle='-', color='b')
plt.title('Dewpoint Forecast')
plt.xlabel('Time')
plt.ylabel('Dewpoint (°F)')
plt.grid(True)
plt.xticks(rotation=45)

# Display the plot in Streamlit
st.pyplot(plt)