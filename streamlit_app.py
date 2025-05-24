import streamlit as st
import login
import register
import requests
import ai_recommendation
import egzersiz_takibi
import sensor_data

# Sayfa başlığı ve ikon ayarları
st.set_page_config(page_title="MuscleTrack", page_icon="💪")

# Backend API adresi
API_URL = "https://muscletrack.onrender.com"

# ✅ Yeni query param API kullanımı
params = st.query_params
page = params.get("page", "login")

# Oturum kontrolü
logged_in = st.session_state.get("logged_in", False)

# Giriş yapılmamışsa sadece login ve register'a izin ver
if not logged_in and page not in ["login", "register"]:
    st.query_params.update({"page": "login"})
    st.rerun()

# Giriş yapılmışsa login/register'dan diğer sayfalara yönlendir
if logged_in and page in ["login", "register"]:
    st.query_params.update({"page": "sensor_data"})
    st.rerun()

# (Geliştirme amacıyla) Kullanıcı adı konsola yazdırılsın
if "username" in st.session_state:
    print("Kullanıcı:", st.session_state["username"])

# Ana sayfa yönlendirme
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

# 🔘 Sidebar menü ve çıkış butonu
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
        st.query_params.update({"page": sayfa_dict[secim]})
        st.rerun()

    if st.sidebar.button("❌ Çıkış Yap"):
        st.session_state.clear()
        st.query_params.update({"page": "login"})
        st.rerun()
