import streamlit as st

# Sayfa yapılandırması
st.set_page_config(page_title="Egzersiz Takibi", page_icon="👣")

# Başlık ve açıklama
st.title("Egzersiz Takibi")
st.write("Bu sayfada egzersizlerinizi takip edebilir, ilerlemenizi görebilirsiniz.")


if not st.session_state.get("logged_in"):
    st.warning("Lütfen egzersizleri görebilmek için giriş yapın.")
    st.stop()


# Kullanıcı adı (güncellendi)
kullanici_adi = st.session_state["username"]
st.title("Egzersiz Takibi")
st.write(f"Hoş geldin **{kullanici_adi}**! Bu sayfada egzersizlerini takip edebilir, ilerlemeni görebilirsin.")

# 🎯 Egzersiz ilerleme takibi
if "tamamlanan_egzersiz" not in st.session_state:
    st.session_state["tamamlanan_egzersiz"] = 0

toplam_egzersiz = 2
ilerleme = st.session_state["tamamlanan_egzersiz"] / toplam_egzersiz

st.subheader("İlerlemeniz 🌟")
st.progress(ilerleme)
st.info(f"Toplam {toplam_egzersiz} egzersizden {st.session_state['tamamlanan_egzersiz']} tanesini tamamladınız.")

st.markdown("---")

# 🦵 Egzersiz 1
st.header("🦵 Ayak Bileği Pompası")
st.markdown("""
**Amaç:** Dolaşımı ve bilek hareketini artırmak  
**Yapılışı:** Ayak bileğini ileri geri hareket ettir.  
**Tekrar:** 10-15 tekrar, günde 2-3 kez
""")
if st.button("✅ Yaptım (Ayak Bileği Pompası)"):
    st.session_state["tamamlanan_egzersiz"] += 1
    st.success("Tebrikler! Bir egzersizi tamamladınız. 🌟")
    st.experimental_rerun()

st.markdown("---")

# 🦶 Egzersiz 2
st.header("🦶 Parmak Esnetme")
st.markdown("""
**Amaç:** Parmak kaslarını çalıştırmak  
**Yapılışı:** Ayak parmaklarını ileri ve geri esnet.  
**Tekrar:** 10 tekrar, günde 2 kez
""")
if st.button("✅ Yaptım (Parmak Esnetme)"):
    st.session_state["tamamlanan_egzersiz"] += 1
    st.success("Harika! Bir egzersiz daha tamamlandı. 🌟")
    st.experimental_rerun()

# Sayfa altı notu
st.caption("MuscleTrack – Sağlıklı bir yaşam için egzersiz takibi 💪")
