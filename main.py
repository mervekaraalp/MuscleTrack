import streamlit as st
from pages import login, register, sensor_data, ai_recommendation, egzersiz_gecmisi

st.set_page_config(page_title="MuscleTrack", page_icon="💪")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# URL'den gelen sayfa parametresini kontrol et
query_page = st.query_params.get("page")

# Sayfa yönlendirme mantığı
if st.session_state.logged_in:
    # Giriş yapmış kullanıcılar için menü ve ilk sayfa
    menu = ["Sensör Verileri", "AI Egzersiz Planı", "Egzersiz Geçmişi", "Çıkış Yap"]
    if query_page == "ai_recommendation":
        choice = "AI Egzersiz Planı"
    elif query_page == "egzersiz_gecmisi":
        choice = "Egzersiz Geçmişi"
    else: # Varsayılan olarak sensör verileri
        choice = st.sidebar.selectbox("Navigasyon", menu, index=menu.index("Sensör Verileri") if "Sensör Verileri" in menu else 0)
else:
    # Giriş yapmamış kullanıcılar için menü ve ilk sayfa
    menu = ["Giriş Yap", "Kayıt Ol"]
    if query_page == "register":
        choice = "Kayıt Ol"
    else: # Varsayılan olarak giriş yap
        choice = st.sidebar.selectbox("Navigasyon", menu, index=menu.index("Giriş Yap") if "Giriş Yap" in menu else 0)


# Menü seçeneklerine veya query_params'a göre sayfa içeriği
if choice == "Giriş Yap":
    login.app()
elif choice == "Kayıt Ol":
    register.app()
elif choice == "Sensör Verileri":
    sensor_data.app()
elif choice == "AI Egzersiz Planı":
    ai_recommendation.app()
elif choice == "Egzersiz Geçmişi": # Yeni eklenen sayfa
    egzersiz_gecmisi.app()
elif choice == "Çıkış Yap":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Başarıyla çıkış yaptınız.")
    st.query_params.update({"page": "login"}) # Çıkış yapınca login sayfasına yönlendir
    st.experimental_rerun()
