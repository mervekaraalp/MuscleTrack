import streamlit as st
import requests

# API URL (Render'daki Flask sunucun)
API_URL = "https://muscletrack.onrender.com"

# Başlık
st.set_page_config(page_title="MuscleTrack Giriş", page_icon="💪")
st.title("💪 MuscleTrack Giriş Paneli")

# Giriş yapıldıysa doğrudan yönlendir
if st.session_state.get("logged_in"):
    st.experimental_set_query_params(page="sensor_data")  # URL parametreleri ile yönlendirme
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
                # Giriş yapıldıysa session state güncellenir
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("Giriş başarılı!")
                
                # Sayfa yönlendirmesi: Sensor data sayfasına yönlendir
                st.experimental_set_query_params(page="sensor_data")
                st.stop()
            else:
                st.error("Giriş başarısız! Kullanıcı adı veya şifre hatalı.")
        except Exception as e:
            st.error(f"Hata oluştu: {e}")

# Kayıt bağlantısı
st.info("Hesabınız yok mu?")
if st.button("Kayıt Ol"):
    # Kayıt sayfasına yönlendirme
    st.experimental_set_query_params(page="register")  # Sayfa ismi yerine parametre ekleyerek yönlendirme
    st.stop()



