import streamlit as st
import requests
import pandas as pd

st.title("MuscleTrack Gösterge Paneli")

# Kullanıcı giriş kontrolü
if "token" not in st.session_state:
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

token = st.session_state["token"]
username = st.session_state["username"]

st.success(f"Hoş geldin, {username}!")

# API'den veri çekme
headers = {"x-access-token": token}
response = requests.get("https://muscletrack.onrender.com/sensor_data", headers=headers)  # Render API URL'si

# API yanıtını işleme
if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    
    # Veriyi DataFrame olarak göster
    st.dataframe(df)

    # Veriyi çizimle gösterme
    st.line_chart(df.set_index("timestamp")[["emg", "flex", "value"]])
else:
    st.error("Veri alınamadı. Token süresi dolmuş olabilir.")



