import streamlit as st
from api_client import register_user

st.title("Kayıt Ol")

username = st.text_input("Kullanıcı Adı")
password = st.text_input("Şifre", type="password")

if st.button("Kayıt Ol"):
    result = register_user(username, password)
    if result.get("message") == "Kayıt başarılı!":
        st.success("Kayıt başarılı! Artık giriş yapabilirsiniz.")
    else:
        st.error(result.get("message", "Kayıt başarısız."))
