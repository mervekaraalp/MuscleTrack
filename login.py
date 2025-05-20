import streamlit as st
import requests
import login
import egzersiz_takibi
import ai_recommendation
import sensor_data

st.set_page_config(page_title="MuscleTrack Giriş", page_icon="💪")
st.title("💪 MuscleTrack Giriş Paneli")

API_URL = "https://muscletrack.onrender.com"


# Sidebar menüsü
if logged_in:
    secim = st.sidebar.radio("📋 Sayfa Seç", ["Egzersiz Takibi", "AI Egzersiz", "Sensör Verisi"])
else:
    secim = "Giriş"





def app():
    st.title("💪 MuscleTrack Giriş Paneli")
    # Kullanıcı adı, şifre girişi ve giriş işlemi kodu burada
    # Giriş başarılıysa:
    # st.session_state['logged_in'] = True
    # st.session_state['kullanici_adi'] = girilen_kullanici_adi




# Giriş yapıldıysa yönlendirme
if st.session_state.get("logged_in"):  # burası zaten doğru
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
                # Giriş başarılıysa session_state güncellemesi
                st.session_state["logged_in"] = True  # burası doğru
                st.session_state["username"] = username
                st.success("Giriş başarılı!")

                st.experimental_set_query_params(page="sensor_data")
                st.stop()
            else:
                st.error("Giriş başarısız! Kullanıcı adı veya şifre hatalı.")
        except Exception as e:
            st.error(f"Hata oluştu: {e}")

st.info("Hesabınız yok mu?")
if st.button("Kayıt Ol"):
    st.experimental_set_query_params(page="register")
    st.stop()







