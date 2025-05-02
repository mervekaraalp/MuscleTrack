import streamlit as st
import requests

st.title("MuscleTrack Kullanıcı Paneli")

BASE_URL = "https://muscletrack.onrender.com"


menu = ["Kayıt Ol", "Giriş Yap"]
choice = st.sidebar.selectbox("Menü", menu)

if choice == "Kayıt Ol":
    st.subheader("Kayıt Ol")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    if st.button("Kayıt Ol"):
        try:
            register_response = requests.post(f"{BASE_URL}/register_api", json={
                "username": username,
                "password": password
            })
            if register_response.status_code == 201:
                st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
            else:
                try:
                    response_json = register_response.json()
                    st.error("Kayıt başarısız: " + response_json.get("message", "Hata oluştu."))
                except Exception:
                    st.error(f"Kayıt başarısız! Sunucudan dönen cevap: {register_response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Sunucuya bağlanılamadı. Flask sunucusunun çalıştığından emin olun.")

elif choice == "Giriş Yap":
    st.subheader("Giriş Yap")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        try:
            login_response = requests.post(f"{BASE_URL}/login_api", json={
                "username": username,
                "password": password
            })
            if login_response.status_code == 200:
                token = login_response.json().get("token")
                st.success("Giriş başarılı!")

                # Token ile veri alalım
                headers = {"x-access-token": token}
                data_response = requests.get(f"{BASE_URL}/sensor_data", headers=headers)

                if data_response.status_code == 200:
                    sensor_data = data_response.json().get("sensor_data", [])
                    st.write("Sensör Verileri:")
                    st.dataframe(sensor_data)
                else:
                    st.warning("Sensör verileri alınamadı.")
            else:
                st.error("Giriş başarısız: " + login_response.json().get("message", "Hata oluştu."))
        except requests.exceptions.ConnectionError:
            st.error("Sunucuya bağlanılamadı. Flask sunucusunun çalıştığından emin olun.")

st.session_state.token = token
st.session_state.logged_in = True

if st.session_state.get("logged_in"):
    st.subheader("Sensör Verileri")
    headers = {"x-access-token": st.session_state.token}
    data_response = requests.get(f"{BASE_URL}/sensor_data", headers=headers)
    if data_response.status_code == 200:
        sensor_data = data_response.json().get("sensor_data", [])
        st.dataframe(sensor_data)
    else:
        st.warning("Sensör verileri alınamadı.")
