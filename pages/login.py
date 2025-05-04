import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

API_URL = 'https://muscletrack.onrender.com'  # Render API URL

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
                st.success("Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz.")
                # Giriş sayfasına yönlendirmek için session_state güncellenir
                st.session_state['registered'] = True
            else:
                try:
                    data = response.json()
                    st.error(data.get("message", "Kayıt başarısız."))
                except ValueError:
                    st.error("API'den geçerli bir yanıt alınamadı.")

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
                st.session_state['token'] = token
                st.session_state['username'] = username
                st.session_state['logged_in'] = True
                st.success("Giriş başarılı!")
                switch_page("dashboard")  # Dashboard sayfasına yönlendirme
            else:
                st.error(response.json().get("message", "Giriş başarısız."))

# Çıkış yap fonksiyonu
def logout_user():
    st.session_state.logged_in = False
    st.session_state.pop("token", None)
    st.session_state.pop("username", None)
    st.success("Çıkış yapıldı.")
    # Sayfayı yenileyerek giriş sayfasına dönebiliriz
    st.experimental_rerun()

# Oturum kontrolü
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Giriş yapılmışsa karşılama ve çıkış seçeneği
if st.session_state.logged_in:
    st.write(f"Hoş geldin, {st.session_state.get('username', '')}!")
    if st.button("Çıkış Yap"):
        logout_user()
else:
    page = st.selectbox("Sayfa Seç", ["Giriş Yap", "Kayıt Ol"])
    if page == "Giriş Yap":
        login_user()
    elif page == "Kayıt Ol":
        register_user()

