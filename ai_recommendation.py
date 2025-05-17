import streamlit as st
import random
from database import egzersiz_kaydet

st.set_page_config(page_title="AI Egzersiz Önerisi", page_icon="🧠")

st.title("🧠 AI Destekli Egzersiz Önerisi")
st.markdown("Sensör verilerinizi analiz ederek size en uygun egzersizleri öneriyoruz.")

# Giriş kontrolü
if 'giris_yapildi' not in st.session_state or not st.session_state['giris_yapildi']:
    st.warning("Lütfen önce giriş yapınız.")
    st.stop()

# Kullanıcı adı kontrolü
kullanici_adi = st.session_state.get("username", "Bilinmiyor")

# Vücut bölgesi seçimi
bolge = st.selectbox("Lütfen bir vücut bölgesi seçin:", ["Ayak", "El"])

# Simülasyon - ilgili bölge için veri durumu
veri_durumu = st.selectbox("AI sistemine göre bu bölgede bir sorun var mı?", ["Evet", "Hayır"])

# Egzersiz veritabanı
egzersizler = {
    "Ayak": {
        "Topuk Üzerinde Yükselme": "Topuklar üzerinde yükselip inme. 10 tekrar.",
        "Ayak Bileği Pompası": "Ayak bileğini yukarı-aşağı oynatma. 15 tekrar.",
        "Ayak Parmak Esnetme": "Parmakları ileri-geri hareket ettirme. 10 tekrar.",
        "Bacak Kaldırma": "Bacağı yukarı kaldırıp indirme. 10 tekrar.",
    },
    "El": {
        "Top Sıkma": "Yumuşak bir topu 5 saniye boyunca sıkın, bırakın. 10 tekrar.",
        "Parmak Açma": "Avucunuzu açın ve kapatın. 15 tekrar.",
        "Bilek Döndürme": "Bileğinizi saat yönünde ve ters yönde döndürün. 10 tekrar.",
        "Avuç Genişletme": "Parmakları yana açıp kapatma. 12 tekrar.",
    }
}

# Egzersiz önerileri (AI simülasyonu)
st.markdown(f"### 🤖 Önerilen Egzersizler ({bolge} için):")

if veri_durumu == "Evet":
    st.success(f"AI'ya göre {bolge.lower()} bölgenizde bir sorun olabilir. Aşağıdaki egzersizler önerilmektedir:")
    onerilen = list(egzersizler[bolge].items())[:3]
else:
    st.info(f"{bolge} bölgesinde sorun tespit edilmedi. Genel egzersiz önerileri aşağıda:")
    onerilen = random.sample(list(egzersizler[bolge].items()), 3)

# Listele
for ad, aciklama in onerilen:
    st.markdown(f"- **{ad}**: {aciklama}")

# Egzersizleri kaydet
if st.button("📥 Egzersizleri Günlük Kaydet"):
    egzersiz_kaydet(
        kullanici_adi=kullanici_adi,
        bolge=bolge,
        egzersizler=[ad for ad, _ in onerilen]
    )
    st.success("Egzersiz önerileri başarıyla günlük geçmişinize kaydedildi.")

# Alt bilgi
st.caption("MuscleTrack AI – Sensör destekli akıllı egzersiz rehberi 💪")
