import requests

API_URL = "https://muscletrack.onrender.com"

def login_user(username, password):
    response = requests.post(f"{API_URL}/login_api", json={
        "username": username,
        "password": password
    })
    return response.json()

def register_user(username, password):
    try:
        response = requests.post(f"{API_URL}/register_api", json={
            "username": username,
            "password": password
        })
        return response.json()
    except Exception as e:
        return {"message": f"API hatası: {str(e)}"}



