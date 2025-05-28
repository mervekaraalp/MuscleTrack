import streamlit as st
import requests
import time # time modülünü import edin

# API_URL'i buraya da ekleyebilirsiniz veya global bir yerden alabilirsiniz.
API_URL = "https://muscletrack.onrender.com"

def app():
    # Zaten giriş yapılmışsa doğrudan ana sayfaya yönlendir
    if st.session_state.get('logged_in', False):
        st.info("Zaten giriş yapmışsınız. Ana sayfaya yönlendiriliyorsunuz...")
        st.query_params.update({"page": "sensor_data"}) # Giriş sonrası ana sayfa
        st.rerun()
        return # <-- BURAYI EKLEYİN

    st.title("🔐 Giriş Yap")

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if not username or not password:
            st.error("Kullanıcı adı ve şifre boş bırakılamaz.")
            return # Eksik bilgi varsa daha fazla devam etme

        try:
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})

            if response.status_code == 200:
                data = response.json()
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.token = data.get("token")
                st.success(f"Hoş geldin, {username}!")
                time.sleep(1) # Yönlendirmeden önce kısa bir bekleme
                st.query_params.update({"page": "sensor_data"}) # Başarılı giriş sonrası yönlendirme
                st.rerun()
                return # <-- BURAYI EKLEYİN
            elif response.status_code == 401:
                st.error("Yanlış kullanıcı adı veya şifre.")
            else:
                st.error("Giriş yapılırken bir hata oluştu. Lütfen tekrar deneyin.")
                st.write(f"Hata Kodu: {response.status_code}") # Debug için
                st.write(f"Hata Mesajı: {response.json()}") # Debug için
        except requests.exceptions.RequestException as e:
            st.error(f"Sunucuya bağlanırken hata oluştu: {e}")
            st.info("Lütfen backend API'nizin çalıştığından emin olun.")

    st.markdown("---")
    st.write("Hesabınız yok mu?")
    if st.button("Kayıt Ol"):
        st.query_params.update({"page": "register"}) # Kayıt sayfasına yönlendir
        st.rerun()
        return # <-- BURAYI EKLEYİN
