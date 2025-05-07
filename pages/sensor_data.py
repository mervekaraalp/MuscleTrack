import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt

st.set_page_config(page_title="Sensör Verileri", page_icon="📊")

# Giriş kontrolü (token kullanımı)
if "token" not in st.session_state:
    st.warning("Bu sayfaya erişmek için giriş yapmalısınız.")
    st.stop()

st.title("📊 Sensör Verileri")
st.write("Bu sayfada sensör verilerini izleyebilirsiniz.")

# Kullanıcı adı gösterimi (varsa)
if "username" in st.session_state:
    st.subheader(f"Merhaba, **{st.session_state.username}**!")

# Seçimler
sensor_type = st.radio("Sensör Tipi Seç", ["EMG Kas Sensörü", "Flex Sensörleri"], horizontal=True)
body_part = st.radio("Vücut Bölgesi", ["Ayak", "Bacak"], horizontal=True)
time_range = st.selectbox("Zaman Aralığı", ["Son 7 Gün", "Son 30 Gün", "Tüm Veriler"])

# Tarih hesaplama
today = datetime.today()
if time_range == "Son 7 Gün":
    start_date = today - timedelta(days=7)
elif time_range == "Son 30 Gün":
    start_date = today - timedelta(days=30)
else:
    start_date = today - timedelta(days=365)

num_days = (today - start_date).days
dates = sorted([today - timedelta(days=i) for i in range(num_days)])

# EMG grafiği
if sensor_type == "EMG Kas Sensörü":
    df = pd.DataFrame({
        "Tarih": dates,
        "Vücut Bölgesi": [body_part] * num_days,
        "EMG (mV)": [round(100 + i * 0.5 + (i % 5) * 2.5, 2) for i in range(num_days)]
    })

    st.subheader("📉 EMG Zaman Serisi Grafiği")
    emg_chart = alt.Chart(df).mark_line(point=True).encode(
        x="Tarih:T",
        y="EMG (mV):Q",
        tooltip=["Tarih", "EMG (mV)"]
    ).properties(width=700, height=300)
    st.altair_chart(emg_chart, use_container_width=True)

# Flex grafiği
else:
    df = pd.DataFrame({
        "Tarih": dates,
        "Vücut Bölgesi": [body_part] * num_days,
        "Flex1": [round(20 + (i % 3) * 1.5, 2) for i in range(num_days)],
        "Flex2": [round(25 + (i % 4) * 1.3, 2) for i in range(num_days)],
        "Flex3": [round(30 + (i % 5) * 1.1, 2) for i in range(num_days)],
        "Flex4": [round(22 + (i % 6) * 1.2, 2) for i in range(num_days)],
        "Flex5": [round(28 + (i % 7) * 1.4, 2) for i in range(num_days)]
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

# Tablo
st.subheader("📄 Detaylı Sensör Verileri")
st.dataframe(df.sort_values("Tarih", ascending=False), use_container_width=True)

# Çıkış
if st.button("Çıkış Yap"):
    del st.session_state["token"]
    if "username" in st.session_state:
        del st.session_state["username"]
    st.switch_page("streamlit_app")
