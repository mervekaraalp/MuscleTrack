import requests


BASE_URL = "https://muscletrack.onrender.com"

def login_user(username, password):
    response = requests.post(f"{API_URL}/login", json={
        "username": username,
        "password": password
    })
    return response.json()

def register_user(username, password):
    response = requests.post(f"{API_URL}/register", json={
        "username": username,
        "password": password
    })
    return response.json()
# api_client.py
import requests

API_URL ="https://muscletrack.onrender.com/login_api"


def register_user(username, password):
    try:
        response = requests.post(f"{API_URL}/register", json={
            "username": username,
            "password": password
        })
        return response.json()
    except Exception as e:
        return {"message": f"Bağlantı hatası: {str(e)}"}
