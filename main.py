import requests
from datetime import datetime
import time

# London lat & long
LONDON_LAT = 51.507351
LONDON_LONG = -0.127758


# --------------------------- CHECK IF ISS IS CLOSE TO CURRENT LOCATION ------------------- #
def is_iss_close():
    # get iss data from api
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    # iss_position = (iss_longitude, iss_latitude)
    # check if iss within 5 of current lat and long
    if LONDON_LAT - 5 <= iss_latitude <= LONDON_LAT + 5 and LONDON_LONG - 5 <= iss_longitude <= LONDON_LONG + 5:
        return True


# ---------------------------- GET SUNRISE, SUNSET DATA & CHECK WHETHER IT IS NIGHT  ------------------------------- #

def is_night():
    # formatted turned off gets unix time back
    parameters = {
        "lat": LONDON_LAT,
        "lng": LONDON_LONG,
        "formatted": 0
    }
    # use sunrise-sunset api
    response_sunset_api = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response_sunset_api.raise_for_status()
    data_sunset_api = response_sunset_api.json()
    # format data in float to use it for comparison
    sunrise = data_sunset_api["results"]["sunrise"]
    sunset = data_sunset_api["results"]["sunset"]
    # split data to compare time with current time
    sunrise_time = int(sunrise.split("T")[1].split(":")[0])
    sunset_time = int(sunset.split("T")[1].split(":")[0])
    # get current hour
    time_now = datetime.now().hour
    if time_now >= sunset_time or time_now <= sunrise_time:
        return True


while True:
    time.sleep(60)
    print(f"Time:{datetime.now()}")
    if is_iss_close() and is_night():
        print(f"Look up ISS is in sight - Time:{datetime.now()}")
    else:
        print("ISS not near current location")
    print("--------------------------------------------------------")