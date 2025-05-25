import streamlit as st
import requests

API_URL = "https://muscletrack.onrender.com"

def app():
    st.title("📝 Kayıt Ol")

    if st.session_state.get("logged_in"):
        st.success("Zaten giriş yaptınız, yönlendiriliyorsunuz...")
        st.query_params.update({"page": "sensor_data"})
        st.stop()

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    confirm_password = st.text_input("Şifre (Tekrar)", type="password")

    if st.button("Kayıt Ol"):
        if not username or not password or not confirm_password:
            st.warning("Lütfen tüm alanları doldurun.")
        elif password != confirm_password:
            st.error("Şifreler eşleşmiyor.")
        else:
            try:
                response = requests.post(f"{API_URL}/register_api", json={
                    "username": username,
                    "password": password
                })

                if response.status_code == 201:
                    st.success("Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz...")
                    st.query_params.update({"page": "login"})
                    st.stop()
                elif response.status_code == 409:
                    st.error("Bu kullanıcı adı zaten alınmış.")
                else:
                    st.error("Kayıt başarısız. Lütfen tekrar deneyin.")
            except Exception as e:
                st.error(f"Sunucu hatası: {e}")

    if st.button("🔙 Girişe Dön"):
        st.query_params.update({"page": "login"})
        st.stop()
