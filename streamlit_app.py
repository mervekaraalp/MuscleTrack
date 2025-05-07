import streamlit as st
import requests

# API adresi
API_URL = "https://muscletrack.onrender.com"

# Sayfa ayarları
st.set_page_config(page_title="MuscleTrack", page_icon="💪", layout="centered")

# URL parametresinden sayfa bilgisi al
page = st.query_params.get("page", None)

# Eğer "register" sayfası çağrıldıysa kayıt formunu göster
if page == "register":
    st.title("📝 Kayıt Ol")
    username = st.text_input("Yeni Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Kaydol"):
        try:
            response = requests.post(f"{API_URL}/register_api", json={
                "username": username,
                "password": password
            })

            if response.status_code == 201:
                st.success("Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz.")
                st.query_params.clear()  # URL'den "register" parametresini kaldır
                st.rerun()
            else:
                st.error("Kayıt başarısız. Kullanıcı adı zaten mevcut olabilir.")
        except requests.exceptions.RequestException:
            st.error("API'ye ulaşılamadı.")
    if st.button("Giriş Sayfasına Dön"):
        st.query_params.clear()
        st.rerun()

# Eğer giriş yapılmamışsa giriş ekranını göster
elif "token" not in st.session_state:
    st.title("💪 MuscleTrack Paneli")
    st.markdown("""
    Gerçek zamanlı kas izleme ve rehabilitasyon sürecini takip etme platformu.  
    Devam edebilmek için giriş yapın veya kayıt olun! 👇
    """)
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        try:
            response = requests.post(f"{API_URL}/login_api", json={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                token = response.json()["token"]
                st.session_state.token = token
                st.success("Giriş başarılı!")
                st.rerun()
            else:
                st.error("Kullanıcı adı veya şifre hatalı.")
        except requests.exceptions.RequestException:
            st.error("API sunucusuna bağlanılamadı.")

    if st.button("Kayıt Ol"):
        st.query_params.update({"page": "register"})
        st.rerun()

# Giriş yapılmışsa sensör verilerini göster
else:
    st.subheader("Sensör Verileri")

    headers = {"x-access-token": st.session_state.token}
    try:
        data_response = requests.get(f"{API_URL}/sensor_data", headers=headers)

        if data_response.status_code == 200:
            sensor_data = data_response.json()
            emg = sensor_data.get('emg', "Yok")
            flex = sensor_data.get('flex', "Yok")

            st.metric(label="EMG Değeri", value=emg)
            st.metric(label="Flex Değeri", value=flex)
        else:
            st.error("Sensör verileri alınamadı.")
    except requests.exceptions.RequestException:
        st.error("API'ye ulaşılamadı.")

    if st.button("Çıkış Yap"):
        del st.session_state.token
        st.rerun()












