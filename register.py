import streamlit as st
from api_client import register_user
st.set_page_config(page_title="Kayıt Ol", page_icon="📝")

st.title("Kayıt Ol")

username = st.text_input("Kullanıcı Adı")
password = st.text_input("Şifre", type="password")

if st.button("Kayıt Ol"):
    try:
        result = register_user(username, password)
        message = result.get("message", "")
        if "başarılı" in message.lower():
            st.success("Kayıt başarılı! Artık giriş yapabilirsiniz.")
        else:
            st.error(message or "Kayıt başarısız.")
    except Exception as e:
        st.error(f"Kayıt sırasında bir hata oluştu: {str(e)}")

if 'result' in locals():
    st.write(result)
