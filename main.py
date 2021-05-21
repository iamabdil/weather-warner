import requests
import os
from twilio.rest import Client

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ['API_KEY']
MY_LAT = 51.507351
MY_LONG = -0.127758
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "exclude": "current,minutely,daily",
    "appid": api_key
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data['hourly'][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today, Remember to bring an ☂️.",
        from_=os.environ['TWILIO_NUMBER'],
        to=os.environ['MY_NUMBER']
    )

    print(message.status)



