import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

# API URL (Render'daki Flask sunucun)
API_URL = "https://muscletrack.onrender.com"

# Sayfa ayarları
st.set_page_config(page_title="MuscleTrack", page_icon="💪", layout="centered")

# Başlık
st.title("💪 MuscleTrack Paneli")
st.markdown("""
Gerçek zamanlı kas izleme ve rehabilitasyon sürecini takip etme platformu.  
Devam edebilmek için giriş yapın veya kayıt olun! 👇
""")

# Giriş ekranı
if "token" not in st.session_state and st.session_state.get("page") != "register":
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
                switch_page("1_Sensör_Verileri")
            else:
                st.error("Kullanıcı adı veya şifre hatalı.")

        except requests.exceptions.RequestException:
            st.error("API sunucusuna bağlanılamadı. Lütfen bağlantıyı kontrol edin.")

    # Kayıt olma butonu
    if st.button("Kayıt Ol"):
        st.session_state.page = "register"
        st.rerun()

# Kayıt ekranı
elif st.session_state.get("page") == "register":
    st.subheader("Kayıt Ol")
    new_username = st.text_input("Yeni Kullanıcı Adı")
    new_password = st.text_input("Yeni Şifre", type="password")

    if st.button("Kaydı Tamamla"):
        try:
            response = requests.post(f"{API_URL}/register_api", json={
                "username": new_username,
                "password": new_password
            })

            if response.status_code == 201:
                st.success("Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
                del st.session_state.page
                st.rerun()
            else:
                st.error("Kayıt başarısız. Kullanıcı adı alınmış olabilir.")

        except requests.exceptions.RequestException:
            st.error("API sunucusuna ulaşılamadı.")












