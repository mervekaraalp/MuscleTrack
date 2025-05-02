import streamlit as st
import requests

# Sayfa başlığı
st.set_page_config(page_title="MuscleTrack Login", page_icon="💪")

# Kullanıcı adı ve şifre girişi
st.title("🔐 Giriş Yap")
username = st.text_input("Kullanıcı Adı")
password = st.text_input("Şifre", type="password")

if st.button("Giriş"):
    # Backend'e (API'ye) post isteği gönderiyoruz
    response = requests.post("https://muscletrack.onrender.com/login_api", json={

        "username": username,
        "password": password
    })
    if response.status_code == 200:
        # Giriş başarılı
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("Giriş başarılı! 🎉")
        st.experimental_set_query_params(page="dashboard")
    

    else:
        # Giriş başarısız
        st.error("Kullanıcı adı veya şifre hatalı.")
