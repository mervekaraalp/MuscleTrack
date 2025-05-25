import streamlit as st
from pages import login, register, sensor_data

st.set_page_config(page_title="MuscleTrack", page_icon="💪")

# Oturum başlatma (ilk giriş)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Sidebar menü
menu = ["Giriş Yap", "Kayıt Ol"]
if st.session_state.logged_in:
    menu = ["Sensör Verileri", "Çıkış Yap"]

choice = st.sidebar.selectbox("Navigasyon", menu)

# Menü seçeneklerine göre sayfa içeriği
if choice == "Giriş Yap":
    login.app()

elif choice == "Kayıt Ol":
    register.app()

elif choice == "Sensör Verileri":
    sensor_data.app()

elif choice == "Çıkış Yap":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Başarıyla çıkış yaptınız.")
