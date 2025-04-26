import streamlit as st

# Sayfa başlığı ve yapılandırması
st.set_page_config(page_title="MuscleTrack", page_icon="💪", layout="centered")

# Başlıklar
st.title("💪 MuscleTrack")
st.subheader("Kas Takip Sistemi ile Güçlenin")

# Açıklama
st.markdown("""
MuscleTrack, kas sağlığınızı gerçek zamanlı olarak izler ve iyileşme sürecinizi optimize etmenize yardımcı olur.

🚀 **Özellikler:**
- Gerçek zamanlı kas aktivite takibi  
- Görsel grafiklerle gelişim analizi  
- Giriş yaparak kişisel verilerinize erişim  
- Rehabilitasyon süreçlerinde uzman desteği  
""")

# Görsel
st.image("https://images.unsplash.com/photo-1584467735871-4c4d7c68d4e0", caption="MuscleTrack ile daha sağlıklı bir iyileşme")

# Giriş formu fonksiyonu
def giris_formu():
    with st.form(key="giris_formu"):
        kullanici_adi = st.text_input("Kullanıcı Adı")
        sifre = st.text_input("Şifre", type="password")
        giris_button = st.form_submit_button("🔐 Giriş Yap")

        if giris_button:
            if kullanici_adi == "admin" and sifre == "1234":
                st.session_state["giris_yapildi"] = True
                st.success("Giriş başarılı!")
            else:
                st.error("Kullanıcı adı veya şifre hatalı!")

# Giriş yapılmadıysa giriş formunu göster
if not st.session_state.get("giris_yapildi"):
    giris_formu()
else:
    st.success("Zaten giriş yaptınız.")
    st.info("Devam etmek için üst menüden bir sayfa seçebilirsiniz.")

