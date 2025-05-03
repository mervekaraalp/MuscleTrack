import requests

# API base URL
API_URL = "https://muscletrack.onrender.com"

# Kullanıcı girişi
def login_user(username, password):
    response = requests.post(f"{API_URL}/login_api", json={
        "username": username,
        "password": password
    })
    return response.json()

# Kullanıcı kaydı
def register_user(username, password):
    response = requests.post(f"{API_URL}/register_api", json={
        "username": username,
        "password": password
    })
    return response.json()


