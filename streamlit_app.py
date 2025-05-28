import streamlit as st
import login
import register
import requests # Eğer API_URL'i burada kullanıyorsak kalsın
import ai_recommendation
import egzersiz_takibi
import sensor_data # Bu dosya artık sensör verilerini API'den çekecek
import egzersiz_gecmisi
import exercise
import settings

# Sayfa başlığı ve ikon ayarları
st.set_page_config(page_title="MuscleTrack", page_icon="💪")

# Backend API adresi (isteğe bağlı olarak burada da tanımlayabiliriz)
# API_URL = "https://muscletrack.onrender.com" # Zaten sensor_data.py içinde var, burada tekrar tanımlamak gerekli değil.

# ✅ Yeni query param API kullanımı
params = st.query_params
page = params.get("page", "login") # Varsayılan olarak login

# Oturum kontrolü
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- Ana Navigasyon Mantığı ---

# Eğer kullanıcı giriş yapmamışsa ve yasaklı bir sayfaya gitmeye çalışıyorsa, login'e yönlendir
if not st.session_state.logged_in and page not in ["login", "register"]:
    st.query_params.update({"page": "login"})
    st.rerun()

# Eğer kullanıcı giriş yapmışsa ve hala login/register sayfasındaysa, sensor_data'ya yönlendir
# NOT: Eğer `sensor_data` API'den veri çekiyorsa, bu uygun bir başlangıç sayfasıdır.
if st.session_state.logged_in and page in ["login", "register"]:
    st.query_params.update({"page": "sensor_data"})
    st.rerun()

# ----------------------------

# (Geliştirme amacıyla) Kullanıcı adı konsola yazdırılsın
if "username" in st.session_state and st.session_state["username"]:
    print("Kullanıcı:", st.session_state["username"])

# --- Sayfa Render Etme ---
# URL'deki 'page' parametresine göre ilgili uygulamayı çalıştır.
if page == "login":
    login.app()
elif page == "register":
    register.app()
elif page == "egzersiz_takibi":
    egzersiz_takibi.app()
elif page == "ai_recommendation":
    ai_recommendation.app()
elif page == "sensor_data": # Bu artık ana gösterge paneli görevi görecek
    sensor_data.app()
elif page == "egzersiz_gecmisi":
    egzersiz_gecmisi.app()
elif page == "exercise":
    exercise.app()
elif page == "settings":
    settings.app()
else:
    # Eğer 'page' parametresi geçersizse veya tanımsızsa varsayılan bir sayfaya yönlendirme
    st.query_params.update({"page": "login"})
    st.rerun()


# --- Sidebar Menü ve Çıkış Butonu ---
if st.session_state.logged_in:
    sayfa_dict = {
        "📈 Sensör Verisi": "sensor_data", # Artık burası dashboard görevi görecek
        "🏃 Egzersiz Takibi": "egzersiz_takibi",
        "🤖 AI Egzersiz": "ai_recommendation",
        "📋 Egzersiz Geçmişi": "egzersiz_gecmisi",
        "🤸 Egzersizler": "exercise",
        "⚙️ Ayarlar": "settings"
    }

    # Mevcut URL'deki 'page' parametresini kullanarak varsayılan seçimi ayarla
    current_page_name = next((k for k, v in sayfa_dict.items() if v == page), list(sayfa_dict.keys())[0])
    secim = st.sidebar.radio("📋 Sayfa Seç", list(sayfa_dict.keys()), index=list(sayfa_dict.keys()).index(current_page_name))

    # Sidebar'dan seçim yapıldığında URL'yi güncelle ve uygulamayı yeniden çalıştır
    if sayfa_dict[secim] != page:
        st.query_params.update({"page": sayfa_dict[secim]})
        st.rerun()

    # Çıkış yap butonu sensor_data.py'ye taşındığı için buradan kaldırılabilir,
    # veya hem sidebar'da hem de sensor_data'da olabilir, kullanıcı tercihine bağlı.
    # Ancak en mantıklısı tek yerden çıkış yapmaktır. sidebar daha uygun.
    # Eğer sensor_data.py'den çıkış butonu kaldırılacaksa, buradaki buton aktif olmalı:
    if st.sidebar.button("❌ Çıkış Yap"):
        st.session_state.clear()
        st.query_params.clear()
        st.query_params.update({"page": "login"})
        st.rerun() # st.rerun() yerine experimental_rerun kullanın
