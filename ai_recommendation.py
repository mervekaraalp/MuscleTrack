import streamlit as st
import random

def get_ai_recommendations():
    # Yapay zekâ simülasyonu – gelecekte ML modeliyle değiştirilebilir
    all_exercises = {
        "Plank": "Karın kaslarını güçlendirmek için 30 saniye plank.",
        "Köprü Hareketi": "Kalçayı güçlendirmek için 10 tekrar köprü hareketi.",
        "Squat": "Bacak kaslarını güçlendirmek için 15 squat.",
        "Lunge": "Her bacak için 10 tekrar lunge.",
        "Diz Germe": "Diz düzken ayağı yukarı kaldırıp tutma. 10 saniye × 3.",
        "Topuk Üzerinde Yükselme": "Topuklar üzerinde yükselip inme. 10 tekrar.",
    }

    # Kullanıcıya özel öneri örneği (rastgele 3 öneri)
    selected = random.sample(list(all_exercises.items()), k=3)
    return dict(selected)

def app():
    st.markdown(f"## Merhaba, **{st.session_state.get('username', 'Misafir')}**! 🤖")
    st.markdown("Aşağıda sana özel olarak önerilen AI destekli egzersiz planı yer alıyor.")

    # AI önerilerini getir
    ai_egzersizler = get_ai_recommendations()

    if 'tamamlanan_ai_egzersizler' not in st.session_state:
        st.session_state['tamamlanan_ai_egzersizler'] = []

    for egzersiz, aciklama in ai_egzersizler.items():
        with st.expander(egzersiz):
            st.write(aciklama)
            if egzersiz not in st.session_state['tamamlanan_ai_egzersizler']:
                if st.button(f"{egzersiz} - Yapıldı ✅"):
                    st.session_state['tamamlanan_ai_egzersizler'].append(egzersiz)
                    st.success(f"{egzersiz} tamamlandı!")
                    st.experimental_rerun()
            else:
                st.info("Bu AI egzersizini zaten tamamladınız 🎉")

    if st.session_state['tamamlanan_ai_egzersizler']:
        st.markdown("### 🤖 Tamamladığınız AI Egzersizleri:")
        for egz in st.session_state['tamamlanan_ai_egzersizler']:
            st.markdown(f"- {egz}")

    if st.button("📁 AI Egzersiz Verilerini Kaydet"):
        st.success("AI destekli egzersiz verileri kaydedildi!")

    st.caption("MuscleTrack – Yapay Zekâ ile kişisel egzersiz önerileri 💡")



