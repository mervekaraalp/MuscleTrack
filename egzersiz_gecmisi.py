import streamlit as st
from database import egzersiz_gecmisi_getir

st.set_page_config(page_title="Egzersiz Geçmişi", page_icon="📚")

st.title("📚 Egzersiz Geçmişi")

if 'giris_yapildi' not in st.session_state or not st.session_state['giris_yapildi']:
    st.warning("Lütfen önce giriş yapınız.")
    st.stop()

kullanici = st.session_state["kullanici_adi"]
gecmis = egzersiz_gecmisi_getir(kullanici)

if not gecmis:
    st.info("Henüz kayıtlı bir egzersiz geçmişiniz bulunmamaktadır.")
else:
    for kayit in reversed(gecmis):
        st.markdown(f"**📅 {kayit['tarih']}** – **{kayit['bolge']} bölgesi** için önerilen egzersizler:")
        for egzersiz in kayit['egzersizler']:
            st.markdown(f"- {egzersiz}")
        st.markdown("---")
