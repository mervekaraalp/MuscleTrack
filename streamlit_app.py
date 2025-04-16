import streamlit as st
import requests

st.set_page_config(page_title="MuscleTrack", page_icon="💪", layout="centered")

st.title("💪 MuscleTrack Dashboard")
st.write("Real-time muscle monitoring for rehabilitation and progress tracking.")

# Giriş ekranı
if "token" not in st.session_state:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post("http://127.0.0.1:5000/login_api", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            token = response.json()["token"]
            st.session_state.token = token
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Giriş yapıldıysa veri göster
else:
    st.subheader("Sensor Data")

    headers = {"x-access-token": st.session_state.token}
    data_response = requests.get("http://127.0.0.1:5000/sensor_data", headers=headers)

    if data_response.status_code == 200:
        sensor_data = data_response.json()
        emg = sensor_data['emg']
        flex = sensor_data['flex']

        st.metric(label="EMG Value", value=emg)
        st.metric(label="Flex Value", value=flex)
    else:
        st.error("Unable to fetch sensor data. Check API status.")

    if st.button("Logout"):
        del st.session_state.token
        st.experimental_rerun()

