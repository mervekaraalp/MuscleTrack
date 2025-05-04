import streamlit as st
import requests

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
            # Kullanıcı adı daha önce kaydedilmiş mi?
            response = requests.get(f"{API_URL}/check_user_exists", params={'username': username})
            if response.status_code == 200 and response.json()['exists']:
                st.error("Bu kullanıcı adı zaten mevcut. Lütfen başka bir kullanıcı adı seçin.")
            else:
                # Yeni kullanıcı kaydı işlemi
                response = requests.post(f"{API_URL}/register_api", json={
                    'username': username,
                    'password': password
                })

                if response.status_code == 201:
                    st.success("Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz.")
                    st.session_state.page = "login"  # Kayıt başarılı, giriş sayfasına yönlendirme
                    st.experimental_rerun()
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
                st.session_state.page = "dashboard"  # Giriş başarılı, dashboard'a yönlendirme
                st.experimental_rerun()
            else:
                st.error(response.json().get("message", "Giriş başarısız."))

# Çıkış yap fonksiyonu
def logout_user():
    st.session_state.logged_in = False
    st.session_state.pop("token", None)
    st.session_state.pop("username", None)
    st.session_state.page = "login"  # Çıkış yapıldığında giriş sayfasına yönlendirme
    st.success("Çıkış yapıldı.")
    st.experimental_rerun()

# Oturum kontrolü
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sayfa durumu kontrolü
if 'page' not in st.session_state:
    st.session_state.page = "login"  # Varsayılan olarak giriş sayfası

# Sayfa geçişi
if st.session_state.page == "login":
    page = st.selectbox("Sayfa Seç", ["Giriş Yap", "Kayıt Ol"])
    if page == "Giriş Yap":
        login_user()
    elif page == "Kayıt Ol":
        register_user()

elif st.session_state.page == "dashboard":
    # Dashboard sayfası içeriği
    st.title("Dashboard")
    st.write("Dashboard'a hoş geldiniz!")
    if st.button("Çıkış Yap"):
        logout_user()




