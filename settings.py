import streamlit as st

# Sayfa ayarları
st.set_page_config(page_title="MuscleTrack", page_icon="💪")

# Giriş formu
def giris_formu():
    with st.form(key="giris_formu"):
        kullanici_adi = st.text_input("Kullanıcı Adı")
        sifre = st.text_input("Şifre", type="password")
        giris_button = st.form_submit_button("🔐 Giriş Yap")

        if giris_button:
            if kullanici_adi == "admin" and sifre == "1234":
                st.session_state["logged_in"] = True
                st.session_state["username"] = kullanici_adi
                st.success("Giriş başarılı!")
                st.experimental_rerun()  # Girişten sonra sayfayı yenile
            else:
                st.error("Kullanıcı adı veya şifre hatalı!")

# Sayfa tanımları
def home_sayfasi():
    st.title("🏠 Home Sayfası")
    st.write("Hoş geldiniz, MuscleTrack platformuna!")

def exercise_sayfasi():
    st.title("🏋️‍♀️ Egzersiz Sayfası")
    st.write("Burada egzersizlerinizi takip edebilirsiniz.")

def sensor_data_sayfasi():
    st.title("📈 Sensör Verisi Sayfası")
    st.write("Burada sensör verilerini görebilirsiniz.")

def ayarlar_sayfasi():
    st.title("⚙️ Ayarlar")
    st.write("Kişisel ayarlarınızı bu sayfada düzenleyebilirsiniz.")
    
    username = st.session_state.get("username", "Bilinmiyor")

    st.subheader("👤 Hesap Ayarları")
    st.text_input("Kullanıcı Adı", value=username, disabled=True)
    st.text_input("Şifre", type="password", placeholder="Yeni şifrenizi girin")

    st.subheader("🎨 Tema Tercihleri")
    theme = st.selectbox("Tema Seç", ["Açık", "Koyu", "Sistem Varsayılanı"])

    st.subheader("🔔 Bildirim Ayarları")
    email_notif = st.checkbox("Uygulama içi bildirimleri al", value=True)

    st.subheader("📊 Veri Takibi")
    data_tracking = st.radio("Sensör verileri anonim olarak takip edilsin mi?", ["Evet", "Hayır"], index=0)

    if st.button("💾 Değişiklikleri Kaydet"):
        st.success("Ayarlar başarıyla kaydedildi!")

# Ana menü
menu = ["Home", "Exercise", "Sensor Data", "Ayarlar"]
secim = st.sidebar.radio("Sayfa Seç", menu)

# Çıkış butonu (sidebar'da)
if st.session_state.get("logged_in"):
    if st.sidebar.button("🚪 Çıkış Yap"):
        st.session_state["logged_in"] = False
        st.session_state.pop("username", None)
        st.experimental_rerun()

# Giriş kontrolü ve sayfa yönlendirme
if not st.session_state.get("logged_in"):
    if secim != "Home":
        st.warning("Lütfen önce giriş yapın.")
    giris_formu()
else:
    if secim == "Home":
        home_sayfasi()
    elif secim == "Exercise":
        exercise_sayfasi()
    elif secim == "Sensor Data":
        sensor_data_sayfasi()
    elif secim == "Ayarlar":
        ayarlar_sayfasi()
