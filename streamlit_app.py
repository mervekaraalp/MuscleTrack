import streamlit as st
import requests

# ⛳️ İlk st. komutu bu olmalı:
st.set_page_config(page_title="MuscleTrack Giriş", page_icon="💪")

# Query parametresinden sayfa bilgisini al
params = st.query_params
page = params.get("page", "login")

# API URL (Flask sunucusu)
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
                response = requests.post(f"{API_URL}/login_api", json={
                    "username": username,
                    "password": password
                })

                if response.status_code == 200:
                    token = response.json().get("token")
                    if token:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.session_state["token"] = token
                        st.success("Giriş başarılı!")
                        st.query_params.update({"page": "sensor_data"})
                        st.rerun()
                    else:
                        st.error("Token alınamadı.")
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
    st.title("📝 Kayıt Sayfası")
    st.write("Yeni kullanıcı kaydını tamamlayın...")

    new_username = st.text_input("Kullanıcı Adı (Yeni)")
    new_password = st.text_input("Şifre", type="password")
    confirm_password = st.text_input("Şifreyi Onayla", type="password")

    if st.button("Kaydı Tamamla"):
        if not new_username or not new_password or not confirm_password:
            st.warning("Lütfen tüm alanları doldurun.")
        elif new_password != confirm_password:
            st.warning("Şifreler uyuşmuyor.")
        else:
            try:
                response = requests.post(f"{API_URL}/register_api", json={
                    "username": new_username,
                    "password": new_password
                })

                if response.status_code == 201:
                    st.success("Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz...")
                    st.query_params.update({"page": "login"})
                    st.rerun()
                elif response.status_code == 409:
                    st.error("Bu kullanıcı adı zaten mevcut.")
                else:
                    st.error("Kayıt başarısız. Lütfen tekrar deneyin.")
            except Exception as e:
                st.error(f"Hata oluştu: {e}")
