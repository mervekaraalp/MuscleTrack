import streamlit as st

# Genel Ayarlar
st.set_page_config(page_title="MuscleTrack", layout="wide", page_icon="💪")

import requests
import ai_recommendation
import login
import egzersiz_takibi
import sensor_data
import register

# Backend API adresi
API_URL = "https://muscletrack.onrender.com"

# Sayfa Parametresi
params = st.query_params
page = params.get("page", "login")

# Oturum Kontrolü
logged_in = st.session_state.get("logged_in", False)

# 🛑 Giriş yapılmamışsa login ve register dışındaki sayfalara erişimi engelle
if not logged_in and page not in ["login", "register"]:
    st.experimental_set_query_params(page="login")
    st.rerun()

# ✅ Giriş yapılmışsa login/register sayfalarından yönlendir
if logged_in and page in ["login", "register"]:
    st.experimental_set_query_params(page="sensor_data")
    st.rerun()

# Kullanıcı adı konsola yazdırılsın (geliştirme amaçlı)
if "username" in st.session_state:
    print("Kullanıcı:", st.session_state["username"])

# Sayfa Yönlendirme
if page == "login":
    login.app()
elif page == "register":
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

# Sidebar Menü ve Çıkış
if logged_in:
    sayfa_dict = {
        "🏃 Egzersiz Takibi": "egzersiz_takibi",
        "🤖 AI Egzersiz": "ai_recommendation",
        "📈 Sensör Verisi": "sensor_data",
        "📋 Egzersiz Geçmişi": "egzersiz_gecmisi",
        "⚙️ Ayarlar": "settings"
    }

    secim = st.sidebar.radio("📋 Sayfa Seç", list(sayfa_dict.keys()))
    if secim:
        st.experimental_set_query_params(page=sayfa_dict[secim])
        st.rerun()

    if st.sidebar.button("❌ Çıkış Yap"):
        st.session_state.clear()
        st.experimental_set_query_params(page="login")
        st.rerun()
