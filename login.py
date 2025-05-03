import streamlit as st
import requests

API_URL = 'http://127.0.0.1:5000'  # Flask API adresi

# Kullanıcı kaydı
def register_user():
    st.title("Kayıt Ol")

    username = st.text_input("Yeni Kullanıcı Adı")
    password = st.text_input("Yeni Şifre", type="password")

    if st.button("Kayıt Ol"):
        if not username or not password:
            st.error("Lütfen kullanıcı adı ve şifre girin.")
        else:
            response = requests.post(f"{API_URL}/register_api", json={
                'username': username,
                'password': password
            })

            if response.status_code == 201:
                st.success("Kayıt başarılı!")
            else:
                st.error(response.json().get("message", "Kayıt başarısız."))

# Kullanıcı giriş
def login_user():
    st.title("Giriş Yap")

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if not username or not password:
            st.error("Lütfen kullanıcı adı ve şifre girin.")
        else:
            response = requests.post(f"{API_URL}/login_api", json={
                'username': username,
                'password': password
            })

            if response.status_code == 200:
                token = response.json()['token']
                st.session_state['token'] = token  # Token'ı session'a kaydediyoruz
                st.success("Giriş başarılı!")
                st.session_state.logged_in = True
                st.experimental_rerun()  # Sayfayı yenileyerek dashboard'a yönlendirebiliriz
            else:
                st.error(response.json().get("message", "Giriş başarısız."))

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.write("Hoş geldiniz!")
    st.write("Ana sayfaya yönlendiriliyorsunuz...")
else:
    page = st.selectbox("Sayfa Seç", ["Giriş Yap", "Kayıt Ol"])
    if page == "Giriş Yap":
        login_user()
    elif page == "Kayıt Ol":
        register_user()


