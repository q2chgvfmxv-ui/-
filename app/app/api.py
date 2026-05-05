import requests

API_URL = "https://api.exchangerate.host/latest"

def convert(amount, from_cur, to_cur):
    data = requests.get(API_URL, params={"base": from_cur}).json()
    rate = data["rates"][to_cur]
    return amount * rate
