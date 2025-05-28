import streamlit as st
import requests
import time # Bu satırı ekleyin

API_URL = "https://muscletrack.onrender.com"

def app():
    st.title("📝 Kayıt Ol")

    if st.session_state.get("logged_in"):
        st.success("Zaten giriş yaptınız, yönlendiriliyorsunuz...")
        st.query_params.update({"page": "sensor_data"})
        # st.stop() # Bu satırı kaldırın veya yoruma alın
        st.experimental_rerun() # <- Bu satırı ekleyin
        return # Yönlendirme sonrası fonksiyonun geri kalanını çalıştırmamak için

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    confirm_password = st.text_input("Şifre (Tekrar)", type="password")

    if st.button("Kayıt Ol"):
        if not username or not password or not confirm_password:
            st.warning("Lütfen tüm alanları doldurun.")
        elif password != confirm_password:
            st.error("Şifreler eşleşmiyor.")
        else:
            try:
                response = requests.post(f"{API_URL}/register_api", json={
                    "username": username,
                    "password": password
                })

                if response.status_code == 201:
                    st.success("Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz...")
                    time.sleep(1) # Kullanıcının mesajı görmesi için 1 saniye bekleyin
                    st.query_params.update({"page": "login"})
                    # st.stop() # Bu satırı kaldırın veya yoruma alın
                    st.experimental_rerun() # <- Bu satırı ekleyin
                    return # Yönlendirme sonrası fonksiyonun geri kalanını çalıştırmamak için
                elif response.status_code == 409:
                    st.error("Bu kullanıcı adı zaten alınmış.")
                elif response.status_code == 400: # Backend'iniz 400 dönerse bu hata için de kontrol ekleyebilirsiniz
                    st.error("Kayıt başarısız: Eksik veya hatalı bilgi gönderildi veya kullanıcı adı zaten alınmış.")
                else:
                    st.error(f"Kayıt başarısız. Lütfen tekrar deneyin. (Hata Kodu: {response.status_code})")
            except Exception as e:
                st.error(f"Sunucu hatası: {e}")

    if st.button("🔙 Girişe Dön"):
        st.query_params.update({"page": "login"})
        # st.stop() # Bu satırı kaldırın veya yoruma alın
        st.experimental_rerun() # <- Bu satırı ekleyin
        return # Yönlendirme sonrası fonksiyonun geri kalanını çalıştırmamak için
