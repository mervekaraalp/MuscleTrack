import streamlit as st
import requests
import time # time modülünü import edin

# API_URL'i buraya da ekleyebilirsiniz veya global bir yerden alabilirsiniz.
API_URL = "https://muscletrack.onrender.com"

def app():
    # Zaten giriş yapılmışsa doğrudan ana sayfaya yönlendir
    if st.session_state.get('logged_in', False):
        st.info("Zaten giriş yapmışsınız. Ana sayfaya yönlendiriliyorsunuz...")
        st.query_params.update({"page": "sensor_data"})
        st.experimental_rerun()
        return # <-- BURAYI EKLEYİN

    st.title("📝 Yeni Kayıt")

    new_username = st.text_input("Yeni Kullanıcı Adı")
    new_password = st.text_input("Yeni Şifre", type="password")
    confirm_password = st.text_input("Şifreyi Onayla", type="password")

    if st.button("Kayıt Ol"):
        if not new_username or not new_password or not confirm_password:
            st.error("Tüm alanları doldurmanız gerekmektedir.")
            return

        if new_password != confirm_password:
            st.error("Şifreler uyuşmuyor.")
            return

        try:
            response = requests.post(f"{API_URL}/register_api", json={"username": new_username, "password": new_password})

            if response.status_code == 201:
                st.success("Kayıt başarılı! Lütfen giriş yapın.")
                time.sleep(1) # Yönlendirmeden önce kısa bir bekleme
                st.query_params.update({"page": "login"}) # Başarılı kayıt sonrası login'e yönlendir
                st.experimental_rerun()
                return # <-- BURAYI EKLEYİN
            elif response.status_code == 409: # Kullanıcı zaten varsa 409 Conflict
                st.error("Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı deneyin.")
            else:
                st.error("Kayıt olunurken bir hata oluştu. Lütfen tekrar deneyin.")
                st.write(f"Hata Kodu: {response.status_code}") # Debug için
                st.write(f"Hata Mesajı: {response.json()}") # Debug için
        except requests.exceptions.RequestException as e:
            st.error(f"Sunucuya bağlanırken hata oluştu: {e}")
            st.info("Lütfen backend API'nizin çalıştığından emin olun.")

    st.markdown("---")
    st.write("Zaten bir hesabınız var mı?")
    if st.button("Girişe Dön"):
        st.query_params.update({"page": "login"}) # Giriş sayfasına geri dön
        st.rerun()
        return # <-- BURAYI EKLEYİN
