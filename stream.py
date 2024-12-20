import pydeck as pdk
import streamlit as st
import matplotlib.pyplot as plt
import utils
from utils import getNWS, get_location


# Display the HTML
st.components.v1.html(get_location, height=0)

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

gif_url = 'https://weather.rap.ucar.edu/model/eta69hr_sfc_prcp.gif'

st.title("12-HR Accumulated Precipitation")
st.markdown("![Mountain Weather Forecast](https://weather.rap.ucar.edu/model/eta12hr_sfc_prcp.gif)")