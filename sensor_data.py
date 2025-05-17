import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt

st.set_page_config(page_title="Sensör Verileri", page_icon="📊")

# Giriş kontrolü (token kontrolü)
if "token" not in st.session_state:
    st.warning("Bu sayfaya erişmek için giriş yapmalısınız.")
    st.stop()

st.title("📊 Sensör Verileri")
st.write("Bu sayfada sensör verilerini izleyebilirsiniz.")

# Kullanıcı adı gösterimi (varsa)
if "username" in st.session_state:
    st.subheader(f"Merhaba, **{st.session_state['username']}**!")

# Kullanıcıdan seçimler al
sensor_type = st.radio("Sensör Tipi Seç", ["EMG Kas Sensörü", "Flex Sensörleri"], horizontal=True)
body_part = st.radio("Vücut Bölgesi", ["Ayak", "Bacak"], horizontal=True)
time_range = st.selectbox("Zaman Aralığı", ["Son 7 Gün", "Son 30 Gün", "Son 365 Gün"])

# Tarih hesaplama
today = datetime.today().date()
if time_range == "Son 7 Gün":
    start_date = today - timedelta(days=7)
elif time_range == "Son 30 Gün":
    start_date = today - timedelta(days=30)
else:
    start_date = today - timedelta(days=365)

num_days = (today - start_date).days
# Tarih listesini kronolojik (artan) sırada oluştur
dates = [start_date + timedelta(days=i) for i in range(num_days + 1)]

# Sensör verisi oluşturma (örnek veriler)
if sensor_type == "EMG Kas Sensörü":
    df = pd.DataFrame({
        "Tarih": dates,
        "Vücut Bölgesi": [body_part] * len(dates),
        "EMG (mV)": [round(100 + i * 0.5 + (i % 5) * 2.5, 2) for i in range(len(dates))]
    })

    st.subheader("📉 EMG Zaman Serisi Grafiği")
    emg_chart = alt.Chart(df).mark_line(point=True).encode(
        x="Tarih:T",
        y="EMG (mV):Q",
        tooltip=["Tarih", "EMG (mV)"]
    ).properties(width=700, height=300)
    st.altair_chart(emg_chart, use_container_width=True)

else:
    df = pd.DataFrame({
        "Tarih": dates,
        "Vücut Bölgesi": [body_part] * len(dates),
        "Flex1": [round(20 + (i % 3) * 1.5, 2) for i in range(len(dates))],
        "Flex2": [round(25 + (i % 4) * 1.3, 2) for i in range(len(dates))],
        "Flex3": [round(30 + (i % 5) * 1.1, 2) for i in range(len(dates))],
        "Flex4": [round(22 + (i % 6) * 1.2, 2) for i in range(len(dates))],
        "Flex5": [round(28 + (i % 7) * 1.4, 2) for i in range(len(dates))]
    })

    st.subheader("📈 Flex Sensörleri Grafiği")
    flex_df = df.melt(id_vars=["Tarih"], value_vars=["Flex1", "Flex2", "Flex3", "Flex4", "Flex5"],
                      var_name="Sensör", value_name="Değer")
    flex_chart = alt.Chart(flex_df).mark_line(point=True).encode(
        x="Tarih:T",
        y="Değer:Q",
        color="Sensör:N",
        tooltip=["Tarih", "Sensör", "Değer"]
    ).properties(width=700, height=300)
    st.altair_chart(flex_chart, use_container_width=True)

# Veri tablosu
st.subheader("📄 Detaylı Sensör Verileri")
st.dataframe(df.sort_values("Tarih", ascending=False), use_container_width=True)

# Çıkış butonu
if st.button("Çıkış Yap"):
    # Oturumdan token ve kullanıcı adını sil
    if "token" in st.session_state:
        del st.session_state["token"]
    if "username" in st.session_state:
        del st.session_state["username"]
    # Sayfayı yenileyerek giriş sayfasına yönlendirme
    st.experimental_rerun()
