import requests
from datetime import datetime
import os

# replit -> https://replit.com/@shagunsharma21/workout-tracker?outputonly=1&lite=true
# googlesheet link ->https://docs.google.com/spreadsheets/d/1Zxw6WoZ2uMOgZoT_P5V2nYQzcxdCBuSZaBxneJXVR9w/edit#gid=0
GENDER = "male"
WEIGHT_KG = "69"
HEIGHT_CM = "184"
AGE = 21

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"] #environment variables

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEET_ENDPOINT"]

exercise_text = input("Tell me which exercises you did: ")

headers = {
  "x-app-id": APP_ID,
  "x-app-key": API_KEY,
}

parameters = {
  "query": exercise_text,
  "gender": GENDER,
  "weight_kg": WEIGHT_KG,
  "height_cm": HEIGHT_CM,
  "age": AGE
}

bearer_headers = {"Authorization": os.environ["TOKEN"]}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
  sheet_inputs = {
    "workout": {
      "date": today_date,
      "time": now_time,
      "exercise": exercise["name"].title(),
      "duration": exercise["duration_min"],
      "calories": exercise["nf_calories"]
    }
  }

  sheet_response = requests.post(sheet_endpoint,
                                 json=sheet_inputs,
                                 headers=bearer_headers)

  print(sheet_response.text)
