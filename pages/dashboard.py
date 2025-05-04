import streamlit as st
import requests
import pandas as pd

st.title("📊 MuscleTrack Gösterge Paneli")

# Kullanıcı giriş kontrolü
if "token" not in st.session_state or "username" not in st.session_state:
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

# Oturum bilgileri
token = st.session_state["token"]
username = st.session_state["username"]

st.success(f"👋 Hoş geldin, {username}!")

# API'den veri çekme
headers = {"x-access-token": token}
response = requests.get("https://muscletrack.onrender.com/sensor_data", headers=headers)

# API yanıtını işleme
if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    # Eğer veri geldiyse işle
    if not df.empty:
        # Zaman damgasını zaman formatına çevir
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")  # Tarihe göre sırala

        # Veriyi tablo olarak göster
        st.subheader("📄 Sensör Verileri")
        st.dataframe(df)

        # Çizgi grafiği ile gösterim
        st.subheader("📈 Zaman Serisi Grafiği")
        st.line_chart(df.set_index("timestamp")[["emg", "flex", "value"]])
    else:
        st.info("Henüz gösterilecek sensör verisi yok.")
else:
    st.error("Veri alınamadı. Oturum süresi dolmuş olabilir, lütfen tekrar giriş yapın.")


