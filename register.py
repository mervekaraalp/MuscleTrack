import streamlit as st
from api_client import register_user

st.title("📝 Kayıt Ol")
st.markdown("Yeni bir hesap oluşturmak için aşağıdaki bilgileri doldurun.")

# Giriş alanları
username = st.text_input("👤 Kullanıcı Adı")
password = st.text_input("🔒 Şifre", type="password")

# Kayıt butonu
if st.button("Kayıt Ol"):
    if username and password:
        try:
            result = register_user(username, password)
            message = result.get("message", "")
            if "başarılı" in message.lower():
                st.success("✅ Kayıt başarılı! Artık giriş yapabilirsiniz.")
            else:
                st.error(message or "❌ Kayıt başarısız.")
        except Exception as e:
            st.error(f"🚨 Kayıt sırasında bir hata oluştu: {str(e)}")
    else:
        st.warning("Lütfen tüm alanları doldurun.")

