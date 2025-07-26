import requests
from django.conf import settings

# Replace with your actual values
CLIENT_ID = settings.FLUTTERWAVE_CLIENT_ID_KEY
CLIENT_SECRET = settings.FLUTTERWAVE_CLIENT_SECRET_KEY
TOKEN_URL = settings.FLUTTERWAVE_TOKEN_URL_SECREY

def get_access_token():
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('access_token')
    else:
        print("Error getting token:", response.text)
        return None