import streamlit as st
import requests

# ⛳️ İlk st. komutu bu olmalı:
st.set_page_config(page_title="MuscleTrack Giriş", page_icon="💪")

# Query parametresinden sayfa bilgisini al
params = st.query_params
page = params.get("page", "login")

# API URL (Flask sunucun)
API_URL = "https://muscletrack.onrender.com"

# Giriş yapılmışsa doğrudan yönlendir
if st.session_state.get("logged_in"):
    st.query_params.update({"page": "sensor_data"})
    st.rerun()

# Giriş Sayfası
if page == "login":
    st.title("💪 MuscleTrack Giriş Paneli")

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if not username or not password:
            st.warning("Lütfen tüm alanları doldurun.")
        else:
            try:
                response = requests.post(f"{API_URL}/login", json={
                    "username": username,
                    "password": password
                })

                if response.status_code == 200:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.success("Giriş başarılı!")
                    st.query_params.update({"page": "sensor_data"})
                    st.rerun()
                else:
                    st.error("Giriş başarısız! Kullanıcı adı veya şifre hatalı.")
            except Exception as e:
                st.error(f"Hata oluştu: {e}")

    st.info("Hesabınız yok mu?")
    if st.button("Kayıt Ol"):
        st.query_params.update({"page": "register"})
        st.rerun()

# Kayıt Sayfası
elif page == "register":
    st.title("Kayıt Sayfası")
    st.write("Yeni kullanıcı kaydını tamamlayın...")














