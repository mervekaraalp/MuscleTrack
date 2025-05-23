import streamlit as st
import requests

API_URL = "https://muscletrack.onrender.com"

def app():
    st.title("📝 Yeni Hesap Oluştur")

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Kaydol"):
        if not username or not password:
            st.warning("Lütfen kullanıcı adı ve şifre girin.")
        else:
            try:
                response = requests.post(f"{API_URL}/register_api", json={
                    "username": username,
                    "password": password
                })

                if response.status_code == 201:
                    st.success("Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz...")
                    st.experimental_set_query_params(page="login")
                    st.stop()
                elif response.status_code == 400:
                    st.error(response.json().get("message", "Geçersiz kayıt verisi."))
                else:
                    st.error("Bilinmeyen bir hata oluştu.")
            except requests.exceptions.RequestException:
                st.error("API'ye bağlanılamadı. Lütfen bağlantınızı kontrol edin.")
