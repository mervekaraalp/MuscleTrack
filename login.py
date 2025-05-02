import streamlit as st
import requests

# Sayfa başlığı
st.set_page_config(page_title="MuscleTrack Login", page_icon="💪")

# Kullanıcı adı ve şifre girişi
st.title("🔐 Giriş Yap")
username = st.text_input("Kullanıcı Adı")
password = st.text_input("Şifre", type="password")
if st.button("Giriş"):
    try:
        response = requests.post("https://muscletrack.onrender.com/login_api", json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Giriş başarılı! 🎉")
            st.experimental_set_query_params(page="dashboard")
        else:
            st.error("Kullanıcı adı veya şifre hatalı.")
    except requests.exceptions.RequestException as e:
        st.error("Sunucuya ulaşılamıyor. Lütfen daha sonra tekrar deneyin.")
        st.exception(e)


if st.session_state.get("logged_in"):
    st.success("Zaten giriş yaptınız.")
    st.experimental_set_query_params(page="dashboard")
