import streamlit as st
import requests

API_URL = 'https://muscletrack.onrender.com'  # Render API URL'si

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
                st.session_state['token'] = token  # Token'ı session'a kaydediyoruz
                st.success("Giriş başarılı!")
                st.session_state.logged_in = True
                st.experimental_rerun()  # Sayfayı yenileyerek dashboard'a yönlendirilebiliriz
            else:
                st.error(response.json().get("message", "Giriş başarısız."))

# Çıkış yap (logout) fonksiyonu
def logout_user():
    st.session_state.logged_in = False
    st.session_state.pop("token", None)  # Token'ı session'dan kaldırıyoruz
    st.success("Çıkış yapıldı. Giriş yapmanız gerekiyor.")
    st.experimental_rerun()  # Sayfayı yenileyerek giriş ekranına yönlendiriyoruz

# Oturum kontrolü
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Kullanıcı girişi yapılmışsa gösterilecek içerik
if st.session_state.logged_in:
    st.write("Hoş geldiniz!")
    if st.button("Çıkış Yap"):
        logout_user()  # Çıkış yap butonuna tıklanırsa logout_user fonksiyonu çalışacak
else:
    page = st.selectbox("Sayfa Seç", ["Giriş Yap", "Kayıt Ol"])
    if page == "Giriş Yap":
        login_user()
    elif page == "Kayıt Ol":
        register_user()
