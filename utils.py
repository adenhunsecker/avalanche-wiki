import requests
import pandas as pd
import json
import os

def main():
    longitude = 43.7328149
    latitude = -111.0904983
    getNWS(longitude, latitude)


def getNWS(longitude, latitude):

    base_url = f'https://api.weather.gov/points/{longitude},{latitude}'

    response = requests.get(base_url)

    data = response.json()

    forecast_url = data["properties"]["forecastGridData"]
    
    forecast_response = requests.get(forecast_url)


    dewPoint = getDewPoint(forecast_response.json())

    data = forecast_response.json()


    return data, dewPoint

    # print(data)

def getDewPoint(data):
    times = [entry['validTime'] for entry in data["properties"]['dewpoint']['values']]
    dewpoint_values = [entry['value'] for entry in data["properties"]['dewpoint']['values']]

    # Clean up the time format to parse into datetime
    valid_times = []
    for time in times:
        clean_time = time.split('/')[0]
        valid_times.append(clean_time)

    dates = pd.to_datetime(valid_times)

    # Convert Celcius to Fahrenheit
    fahrenheit = []
    for value in dewpoint_values:
        f_value = (value * 2) + 30
        fahrenheit.append(f_value) 


    df = pd.DataFrame({
    'DateTime': dates,
    'Dewpoint (°F)': fahrenheit
    })
    
    return df



if __name__ == '__main__':
    main()


# HTML and JavaScript to get user location
get_location = """
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
