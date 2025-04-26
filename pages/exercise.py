import streamlit as st
from datetime import datetime
import os

# Sayfa yapılandırması
st.set_page_config(page_title="Egzersiz Sayfası", page_icon="🏋️")

# Giriş kontrolü
if 'giris_yapildi' not in st.session_state or not st.session_state["giris_yapildi"]:
    st.warning("Lütfen önce giriş yapınız.")
    st.stop()  # Giriş yapılmadıysa, sayfanın geri kalanını çalıştırma

# Giriş yapan kullanıcıyı selamla
st.markdown(f"## Merhaba, **{st.session_state['username']}**! 👋")
st.markdown("Aşağıda günlük egzersiz planınızı bulabilirsiniz. Her egzersizi tamamladığınızda 'Yapıldı' butonuna basmayı unutmayın!")

# Egzersiz listesi (Yeni egzersizler eklendi)
egzersizler = {
    "Bacak Kaldırma": "Bacağınızı yukarı kaldırıp indirme hareketi. 10 tekrar.",
    "Ayak Bileği Pompası": "Ayak bileğini yukarı-aşağı oynatma. 15 tekrar.",
    "Parmak Açma/Kapama": "Parmakları açıp kapama. 3 set.",
    "Diz Germe": "Diz düzken ayağı yukarı kaldırıp tutma. 10 saniye × 3.",
    "Topuk Üzerinde Yükselme": "Topuklar üzerinde yükselip inme. 10 tekrar.",
    "Plank": """
    **Amaç:** Karın kaslarını güçlendirmek  
    **Yapılışı:** Kollar ve ayak parmakları üzerinde durarak vücudu düz tutun.  
    **Tekrar:** 30 saniye, günde 2-3 kez.
    """,
    "Köprü Hareketi": """
    **Amaç:** Kalça kaslarını güçlendirmek  
    **Yapılışı:** Sırt üstü yatarken dizlerinizi bükün ve kalçanızı yukarı kaldırın.  
    **Tekrar:** 10 tekrar, günde 2-3 kez.
    """,
    "Squat": """
    **Amaç:** Bacak kaslarını güçlendirmek  
    **Yapılışı:** Ayaklarınızı omuz genişliğinde açın ve dizlerinizi bükerek oturma hareketi yapın.  
    **Tekrar:** 15 tekrar, günde 2-3 kez.
    """,
    "Lunge": """
    **Amaç:** Bacak ve kalça kaslarını çalıştırmak  
    **Yapılışı:** Bir bacağınızı öne doğru adım atarak dizlerinizi bükün, sonra geriye dönün.  
    **Tekrar:** 10 tekrar (her bacak için), günde 2 kez.
    """,
}

# Egzersiz tamamlama durumlarını takip etmek için session state kullan
if 'tamamlanan_egzersizler' not in st.session_state:
    st.session_state['tamamlanan_egzersizler'] = []

# Egzersiz kartları
for egzersiz, aciklama in egzersizler.items():
    with st.expander(egzersiz):
        st.write(aciklama)
        if egzersiz not in st.session_state['tamamlanan_egzersizler']:
            if st.button(f"{egzersiz} - Yapıldı ✅"):
                st.session_state['tamamlanan_egzersizler'].append(egzersiz)
                st.success(f"{egzersiz} tamamlandı!")
        else:
            st.info("Bu egzersizi zaten tamamladınız 🎉")

# Tüm egzersizleri gösteren tablo
if st.session_state['tamamlanan_egzersizler']:
    st.markdown("### ✅ Bugün tamamladığınız egzersizler:")
    for egz in st.session_state['tamamlanan_egzersizler']:
        st.markdown(f"- {egz}")

# Kaydet butonu (simülasyon)
if st.button("📁 Egzersiz Verilerini Kaydet"):
    # Bu aşamada bir veritabanına veri gönderilebilir
    st.success("Egzersiz verileri başarıyla kaydedildi!")

# Sayfa altı notu
st.caption("MuscleTrack – Sağlıklı bir yaşam için egzersiz takibi 💪")

