import streamlit as st
import requests

# API adresi (Render üzerindeki Flask uygulaman)
API_URL = "https://muscletrack.onrender.com"

# Sayfa ayarları
st.set_page_config(page_title="MuscleTrack - Kayıt Ol", page_icon="💪", layout="centered")

# Başlık
st.title("💪 Kayıt Ol")

# Kullanıcı adı ve şifre inputları
username = st.text_input("Kullanıcı Adı", value=st.session_state.get("username", ""))
password = st.text_input("Şifre", type="password", value=st.session_state.get("password", ""))

# Kayıt işlemi
if st.button("Kayıt Ol"):
    # Kullanıcı adı ve şifreyi session_state'e kaydedelim
    st.session_state["username"] = username
    st.session_state["password"] = password
    
    # API'ye veri gönderme
    try:
        response = requests.post(f"{API_URL}/register_api", json={
            "username": username,
            "password": password
        })
        
        # Hata ayıklamak için API yanıtını yazdıralım
        st.write("API yanıtı:", response.status_code, response.text)
        
        # API başarılı olursa
        if response.status_code == 201:
            st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
            st.session_state.page = "login"  # Kayıt başarılıysa login sayfasına yönlendir
            st.experimental_rerun()  # Sayfayı yenileyelim
        else:
            # Eğer bir hata varsa, API'den gelen mesajı gösterelim
            st.error("Kayıt başarısız: " + response.json().get("message", "Bilinmeyen hata"))
    
    except requests.exceptions.RequestException as e:
        st.error(f"API'ye bağlanırken bir hata oluştu: {e}")
        


