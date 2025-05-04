import streamlit as st
from database import egzersiz_gecmisi_getir

st.set_page_config(page_title="Egzersiz Geçmişi", page_icon="📚")

st.title("📚 Egzersiz Geçmişi")

# Giriş kontrolü
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Lütfen önce giriş yapınız.")
    st.stop()

username = st.session_state["username"]
gecmis = egzersiz_gecmisi_getir(username)

if not gecmis:
    st.info("Henüz kayıtlı bir egzersiz geçmişiniz bulunmamaktadır.")
else:
    for kayit in reversed(gecmis):
        st.markdown(f"**📅 {kayit['tarih']}** – **{kayit['bolge']} bölgesi** için önerilen egzersizler:")
        for egzersiz in kayit['egzersizler']:
            st.markdown(f"- {egzersiz}")
        st.markdown("---")
