import streamlit as st
from database import egzersiz_gecmisi_getir

def app():
    st.title("📚 Egzersiz Geçmişi")

    # Giriş kontrolü
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("Lütfen önce giriş yapınız.")
        return

    username = st.session_state.get("username")
    if not username:
        st.error("Kullanıcı bilgisi alınamadı, lütfen tekrar giriş yapınız.")
        return

    # Veritabanından geçmişi çek
    try:
        gecmis = egzersiz_gecmisi_getir(username)
    except Exception as e:
        st.error(f"Egzersiz geçmişi alınırken hata oluştu: {e}")
        return

    if not gecmis:
        st.info("Henüz kayıtlı bir egzersiz geçmişiniz bulunmamaktadır.")
    else:
        for kayit in reversed(gecmis):
            tarih = kayit.get('tarih', 'Bilinmeyen Tarih')
            bolge = kayit.get('bolge', 'Bilinmeyen Bölge')
            egzersizler = kayit.get('egzersizler', [])
            
            st.markdown(f"**📅 {tarih}** – **{bolge} bölgesi** için önerilen egzersizler:")
            if egzersizler:
                for egzersiz in egzersizler:
                    st.markdown(f"- {egzersiz}")
            else:
                st.markdown("- Önerilen egzersiz bulunmamaktadır.")
            st.markdown("---")
