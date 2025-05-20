import streamlit as st
import requests
import ai_recommendation
import login
import egzersiz_takibi
import sensor_data
import register


# Genel Ayarlar
st.set_page_config(page_title="MuscleTrack", layout="wide", page_icon="💪")

# API URL
API_URL = "https://muscletrack.onrender.com"



# Query parametresinden sayfa bilgisini al
params = st.query_params
page = params.get("page", "login")

# Oturum kontrolü
logged_in = st.session_state.get("logged_in", False)


# Giriş yapılmışsa ve ana sayfa yükleniyorsa, varsayılan sayfaya yönlendir
if logged_in and page in ["login", "register"]:
    st.query_params.update({"page": "sensor_data"})
    st.rerun()

# Sayfa yönlendirme
if page == "login":
    login.app()

elif page == "register":
    import register
    register.app()

elif page == "egzersiz_takibi":
    egzersiz_takibi.app()

elif page == "ai_recommendation":
    ai_recommendation.app()

elif page == "sensor_data":
    sensor_data.app()

elif page == "egzersiz_gecmisi":
    import egzersiz_gecmisi
    egzersiz_gecmisi.app()

elif page == "exercise":
    import exercise
    exercise.app()

elif page == "settings":
    import settings
    settings.app()

# Sidebar menüsü (giriş yapılmışsa)
if logged_in:
    secim = st.sidebar.radio("📋 Sayfa Seç", [
        ("Egzersiz Takibi", "egzersiz_takibi"),
        ("AI Egzersiz", "ai_recommendation"),
        ("Sensör Verisi", "sensor_data"),
        ("Egzersiz Geçmişi", "egzersiz_gecmisi"),
        ("Ayarlar", "settings")
    ])

    if secim:
        st.query_params.update({"page": secim[1]})
        st.rerun()

# Çıkış butonu (giriş yapılmışsa)
if logged_in:
    if st.sidebar.button("❌ Çıkış Yap"):
        st.session_state.clear()
        st.query_params.update({"page": "login"})
        st.rerun()
