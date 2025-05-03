import streamlit as st
import requests

st.set_page_config(page_title="MuscleTrack Paneli", layout="centered")

BASE_URL = "https://muscletrack.onrender.com"

# Oturum durumu başlat
if "token" not in st.session_state:
    st.session_state.token = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

menu = ["Giriş Yap", "Kayıt Ol"]
choice = st.sidebar.selectbox("Menü", menu)

# Giriş Fonksiyonu
def login_user(username, password):
    try:
        response = requests.post(f"{BASE_URL}/login_api", json={"username": username, "password": password})
        if response.status_code == 200:
            return response.json().get("token")
        else:
            return None
    except:
        return None

# Kayıt Fonksiyonu
def register_user(username, password):
    try:
        response = requests.post(f"{BASE_URL}/register_api", json={"username": username, "password": password})
        return response
    except:
        return None

# Sensör verisi gönderme
def send_sensor_data(token, emg, flex, value):
    headers = {'x-access-token': token}
    data = {"emg": emg, "flex": flex, "value": value}
    response = requests.post(f"{BASE_URL}/sensor_data", json=data, headers=headers)
    return response

# Sensör verisi alma
def get_sensor_data(token):
    headers = {'x-access-token': token}
    response = requests.get(f"{BASE_URL}/sensor_data", headers=headers)
    return response

# Giriş Yap
if choice == "Giriş Yap":
    st.subheader("Giriş Yap")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    
    if st.button("Giriş"):
        token = login_user(username, password)
        if token:
            st.session_state.token = token
            st.session_state.logged_in = True
            st.success("Giriş başarılı!")
        else:
            st.error("Giriş başarısız! Kullanıcı adı veya şifre hatalı.")

# Kayıt Ol
elif choice == "Kayıt Ol":
    st.subheader("Kayıt Ol")
    username = st.text_input("Yeni Kullanıcı Adı")
    password = st.text_input("Yeni Şifre", type="password")

    if st.button("Kayıt Ol"):
        if username and password:
            response = register_user(username, password)
            if response and response.status_code == 201:
                st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
            else:
                try:
                    st.error("Hata: " + response.json().get("message", "Kayıt başarısız!"))
                except:
                    st.error("Sunucu hatası.")
        else:
            st.error("Kullanıcı adı ve şifre boş olamaz.")

# Panel - Girişten sonra görünür
if st.session_state.logged_in:
    st.title("Sensör Veri Paneli")

    st.subheader("Sensör Verisi Gönder")
    emg = st.number_input("EMG", value=0.0)
    flex = st.number_input("Flex", value=0.0)
    value = st.number_input("Value", value=0.0)

    if st.button("Veri Gönder"):
        result = send_sensor_data(st.session_state.token, emg, flex, value)
        if result.status_code == 200:
            st.success("Veri gönderildi!")
        else:
            st.error("Veri gönderilemedi!")

    if st.button("Verileri Göster"):
        result = get_sensor_data(st.session_state.token)
        if result.status_code == 200:
            st.json(result.json())
        else:
            st.warning("Veriler alınamadı.")

