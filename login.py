import streamlit as st
import requests

API_URL = 'https://muscletrack.onrender.com'  # API adresin

def register_user():
    st.subheader("Kayıt Ol")

    username = st.text_input("Yeni Kullanıcı Adı", key="register_username")
    password = st.text_input("Yeni Şifre", type="password", key="register_password")

    if st.button("Kayıt Ol"):
        if not username or not password:
            st.error("Lütfen kullanıcı adı ve şifre girin.")
        else:
            response = requests.post(f"{API_URL}/register_api", json={
                'username': username,
                'password': password
            })

            if response.status_code == 201:
                st.success("Kayıt başarılı! Lütfen giriş yapın.")
                st.session_state["page"] = "login"  # Giriş sekmesine döndür
                st.rerun()
            else:
                try:
                    data = response.json()
                    st.error(data.get("message", "Kayıt başarısız."))
                except ValueError:
                    st.error("Sunucudan geçerli yanıt alınamadı.")

def login_user():
    st.subheader("Giriş Yap")

    username = st.text_input("Kullanıcı Adı", key="login_username")
    password = st.text_input("Şifre", type="password", key="login_password")

    if st.button("Giriş Yap"):
        if not username or not password:
            st.error("Lütfen kullanıcı adı ve şifre girin.")
        else:
            response = requests.post(f"{API_URL}/login_api", json={
                'username': username,
                'password': password
            })

            if response.status_code == 200:
                token = response.json().get("token")
                st.session_state['token'] = token
                st.session_state['username'] = username
                st.session_state['logged_in'] = True
                st.success("Giriş başarılı!")

                # Sayfayı tekrar yükleyerek diğer sayfalarda login bilgisini tanıtır
                st.session_state["page"] = "dashboard"
                st.rerun()
            else:
                st.error(response.json().get("message", "Giriş başarısız."))

# Oturum kontrolü ve sayfa seçimi
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.success(f"Zaten giriş yapıldı: {st.session_state['username']}")
        if st.button("Çıkış Yap"):
            st.session_state.clear()
            st.rerun()
    else:
        page = st.radio("Lütfen Seçin", ["Giriş Yap", "Kayıt Ol"])
        if page == "Giriş Yap":
            login_user()
        else:
            register_user()

main()




