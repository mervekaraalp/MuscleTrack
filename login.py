import streamlit as st
from api_client import login_user

st.title("Giriş Yap")

username = st.text_input("Kullanıcı Adı")
password = st.text_input("Şifre", type="password")

if st.button("Giriş"):
    result = login_user(username, password)
    if "user_id" in result:
        st.success(f"Giriş başarılı! Kullanıcı ID: {result['user_id']}")
        st.session_state["user_id"] = result["user_id"]  # Giriş yapan kullanıcıyı oturumda sakla
    else:
        st.error(result.get("message", "Giriş başarısız"))


