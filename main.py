import streamlit as st

# Sayfa başlığı
st.set_page_config(page_title="MuscleTrack", page_icon="💪")

# Menü
menu = ["Ana Sayfa", "Egzersiz", "Sensör Verileri", "Ayarlar"]
choice = st.sidebar.selectbox("Navigasyon", menu)

# Sayfa içeriği
if choice == "Ana Sayfa":
    st.write("MuscleTrack hakkında daha fazla bilgi.")
elif choice == "Egzersiz":
    st.write("Egzersiz sayfasına hoş geldiniz!")
elif choice == "Sensör Verileri":
    st.write("Sensör verileri sayfasına hoş geldiniz!")
elif choice == "Ayarlar":
    st.write("Ayarlar sayfasına hoş geldiniz!")
