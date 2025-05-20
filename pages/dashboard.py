import streamlit as st
import requests
import pandas as pd
import streamlit as st
import login
import egzersiz_takibi
import ai_recommendation
import sensor_data

st.set_page_config(page_title="MuscleTrack", layout="wide")

# Giriş kontrolü ve sidebar menü
if 'logged_in' in st.session_state and st.session_state['logged_in']:
    secim = st.sidebar.radio("Sayfa Seç", ["Giriş", "Egzersiz Takibi", "AI Egzersiz", "Sensör Verisi"])
else:
    secim = "Giriş"

if secim == "Giriş":
    login.app()
elif secim == "Egzersiz Takibi":
    egzersiz_takibi.app()
elif secim == "AI Egzersiz":
    ai_recommedition.app()
elif secim == "Sensör Verisi":
    sensor_data.app()


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
try:
    response = requests.get("https://muscletrack.onrender.com/sensor_data", headers=headers)
except requests.exceptions.RequestException as e:
    st.error(f"Veri alınırken hata oluştu: {e}")
    st.stop()

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
elif response.status_code == 401:
    st.error("Oturum süresi dolmuş olabilir, lütfen tekrar giriş yapın.")
    # Oturum bilgisini sıfırlayabiliriz
    st.session_state.clear()
    st.stop()
else:
    st.error("Veri alınamadı. Lütfen tekrar deneyin.")
