import streamlit as st

def app():
    st.title("⚙️ Ayarlar")
    st.write("Kişisel ayarlarınızı bu sayfada düzenleyebilirsiniz.")

    username = st.session_state.get("username", "Bilinmiyor")

    st.subheader("👤 Hesap Ayarları")
    st.text_input("Kullanıcı Adı", value=username, disabled=True)
    st.text_input("Şifre", type="password", placeholder="Yeni şifrenizi girin")

    st.subheader("🎨 Tema Tercihleri")
    theme = st.selectbox("Tema Seç", ["Açık", "Koyu", "Sistem Varsayılanı"])

    st.subheader("🔔 Bildirim Ayarları")
    email_notif = st.checkbox("Uygulama içi bildirimleri al", value=True)

    st.subheader("📊 Veri Takibi")
    data_tracking = st.radio("Sensör verileri anonim olarak takip edilsin mi?", ["Evet", "Hayır"], index=0)

    if st.button("💾 Değişiklikleri Kaydet"):
        st.success("Ayarlar başarıyla kaydedildi!")
