import streamlit as st
import requests

# API adresi (Render üzerindeki Flask uygulaman)
API_URL = "https://muscletrack.onrender.com"

# Sayfa ayarları
st.set_page_config(page_title="MuscleTrack", page_icon="💪", layout="centered")

# Başlık
st.title("💪 MuscleTrack Paneli")
st.write("Gerçek zamanlı kas izleme ve rehabilitasyon sürecini takip et!")

# Giriş ekranı
if "token" not in st.session_state:
    st.subheader("Giriş Yap")
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
                st.experimental_rerun()
            else:
                st.error("Kullanıcı adı veya şifre hatalı.")

        except requests.exceptions.RequestException:
            st.error("API sunucusuna bağlanılamadı. Lütfen bağlantıyı kontrol edin.")

    # Kayıt olma sayfasına yönlendirme
    if st.button("Kayıt Ol"):
        st.experimental_set_query_params(page="register")  # Yönlendirme yapılır

# Giriş yaptıktan sonra gösterilecek veriler
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
            st.error("Sensör verileri alınamadı. API anahtarını veya sunucuyu kontrol edin.")

    except requests.exceptions.RequestException:
        st.error("API'ye bağlanılamadı. Lütfen internet bağlantınızı veya sunucuyu kontrol edin.")

    if st.button("Çıkış Yap"):
        del st.session_state.token
        st.experimental_rerun()





