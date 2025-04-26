import streamlit as st

# Sayfa yapılandırması
st.set_page_config(page_title="Egzersiz Takibi", page_icon="👣")

# Başlık ve açıklama
st.title("Egzersiz Takibi")
st.write("Bu sayfada egzersizlerinizi takip edebilir, ilerlemenizi görebilirsiniz.")

# Giriş kontrolü
if "giris_yapildi" in st.session_state and st.session_state["giris_yapildi"]:
    # Giriş yapan kullanıcıyı selamla
    if 'username' not in st.session_state:
        st.session_state['username'] = "Kullanıcı"  # Eğer kullanıcı adı yoksa varsayılan bir değer atayın
    
    st.success(f"Hoş geldin **{st.session_state['username']}** 👋")

    # Kullanıcıya özel ilerleme durumu (örnek)
    st.subheader("İlerlemeniz 🌟")
    st.progress(0.6)  # %60 ilerleme örneği
    st.info("Toplam 6 egzersizden 4 tanesini tamamladınız.")

    st.markdown("---")

    # Egzersiz örneği 1
    st.header("🦵 Ayak Bileği Pompası")
    st.markdown("""
    **Amaç:** Dolaşımı ve bilek hareketini artırmak  
    **Yapılışı:** Ayak bileğini ileri geri hareket ettir.  
    **Tekrar:** 10-15 tekrar, günde 2-3 kez
    """)

    if st.button("✅ Yaptım (Ayak Bileği Pompası)") :
        st.success("Tebrikler! Bir egzersizi tamamladınız. 🌟")

    st.markdown("---")

    # Egzersiz örneği 2
    st.header("🦶 Parmak Esnetme")
    st.markdown("""
    **Amaç:** Parmak kaslarını çalıştırmak  
    **Yapılışı:** Ayak parmaklarını ileri ve geri esnet.  
    **Tekrar:** 10 tekrar, günde 2 kez
    """)

    if st.button("✅ Yaptım (Parmak Esnetme)") :
        st.success("Harika! Bir egzersiz daha tamamlandı. 🌟")
else:
    st.warning("Lütfen egzersizleri görebilmek için giriş yapın.")

# Sayfa altı notu
st.caption("MuscleTrack – Sağlıklı bir yaşam için egzersiz takibi 💪")

