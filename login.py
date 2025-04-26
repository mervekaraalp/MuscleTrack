import streamlit as st
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Kullanıcı verisinin bulunduğu dosya
USER_DATA_FILE = "users.json"

# Eğer kullanıcı verisi dosyası yoksa, oluştur
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as f:
        json.dump({}, f)

# Kullanıcı verilerini yükle
def load_users():
    with open(USER_DATA_FILE, "r") as f:
        users = json.load(f)
    return users

# Kullanıcı verilerini kaydet
def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

# Giriş fonksiyonu
def login(username, password):
    users = load_users()
    if username in users and check_password_hash(users[username], password):
        return True
    else:
        return False

# Kayıt fonksiyonu
def register(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = generate_password_hash(password)
    save_users(users)
    return True

# Sayfa
st.title("Giriş Yap / Kayıt Ol")

menu = st.sidebar.selectbox("Menü", ["Giriş Yap", "Kayıt Ol"])

if menu == "Giriş Yap":
    st.subheader("Giriş Yap")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if login(username, password):
            st.success(f"Hoşgeldin {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Hatalı kullanıcı adı veya şifre.")

elif menu == "Kayıt Ol":
    st.subheader("Kayıt Ol")
    username = st.text_input("Yeni Kullanıcı Adı")
    password = st.text_input("Yeni Şifre", type="password")

    if st.button("Kayıt Ol"):
        if register(username, password):
            st.success("Başarıyla kayıt oldun! Şimdi giriş yapabilirsin.")
        else:
            st.error("Bu kullanıcı adı zaten var.")

