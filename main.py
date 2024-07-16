import requests
from datetime import datetime
import time

MY_LAT = 35.689198
MY_LNG = 51.388973

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG-5 <= iss_longitude <= MY_LNG+5:
        return True


def is_nightime():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrisesunset.io/json", params=parameters)
    response.raise_for_status()

    data = response.json()

    sunrise = int(data["results"]["sunrise"].split(" ")[0].split(":")[0])
    sunset = int(data["results"]["sunset"].split(" ")[0].split(":")[0]) + 12

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_nightime():
        print("ISS is visible for you!")
    else:
        print("ISS is not visible for you!")