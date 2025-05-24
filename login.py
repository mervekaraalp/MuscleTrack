import streamlit as st
import requests

API_URL = "https://muscletrack.onrender.com"

def app():
    st.title("💪 MuscleTrack Giriş Paneli")

    # Giriş yapılmışsa direkt yönlendir
    if st.session_state.get("logged_in"):
        st.success(f"Zaten giriş yaptınız, yönlendiriliyorsunuz...")
        st.experimental_set_query_params(page="sensor_data")
        st.stop()

    # Giriş Formu
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
                    data = response.json()
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["token"] = data.get("token")
                    st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
                    st.experimental_set_query_params(page="sensor_data")
                    st.stop()

                else:
                    st.error("Giriş başarısız! Kullanıcı adı veya şifre hatalı.")
            except Exception as e:
                st.error(f"Sunucu hatası: {e}")

    st.info("Hesabınız yok mu?")
    if st.button("Kayıt Ol"):
        st.experimental_set_query_params(page="register")
        st.stop()
