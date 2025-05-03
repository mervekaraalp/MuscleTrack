import streamlit as st
import requests

st.title("MuscleTrack Giriş & Kayıt")

# Giriş Formu
st.subheader("Giriş Yap")
username = st.text_input("Kullanıcı Adı")
password = st.text_input("Şifre", type="password")

if st.button("Giriş"):
    response = requests.post("http://localhost:5000/login_api", json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        token = response.json().get("token")
        st.success("Giriş başarılı!")
        st.session_state["token"] = token
        st.session_state["username"] = username
        st.switch_page("dashboard.py")
    else:
        st.error(response.json().get("message", "Giriş başarısız."))

# Ayırıcı
st.markdown("---")

# Kayıt Formu
st.subheader("Kayıt Ol")
new_username = st.text_input("Yeni Kullanıcı Adı")
new_password = st.text_input("Yeni Şifre", type="password")

if st.button("Kayıt Ol"):
    if not new_username or not new_password:
        st.error("Tüm alanları doldurmalısınız!")
    else:
        response = requests.post("http://localhost:5000/register_api", json={
            "username": new_username,
            "password": new_password
        })
        if response.status_code == 201:
            st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
        else:
            st.error(response.json().get("message", "Kayıt başarısız."))

