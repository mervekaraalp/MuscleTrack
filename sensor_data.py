import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt
import requests # <-- requests kütüphanesini ekleyin

# API URL'sini burada tanımlayabiliriz veya main.py'den alabiliriz
API_URL = "https://muscletrack.onrender.com"

def app():
    st.title("📊 Sensör Verileri")

    # Giriş kontrolü (token kontrolü)
    if "token" not in st.session_state:
        st.warning("Bu sayfaya erişmek için giriş yapmalısınız.")
        st.query_params.update({"page": "login"})
        st.rerun()
        return

    # Kullanıcı adı gösterimi (varsa)
    if "username" in st.session_state:
        st.subheader(f"Merhaba, **{st.session_state['username']}**!")

    # API'den sensör verisi çekme
    token = st.session_state["token"]
    headers = {"x-access-token": token}

    try:
        response = requests.get(f"{API_URL}/sensor_data", headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            if not df.empty:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                df = df.sort_values("timestamp")

                st.success("Sensör verileri başarıyla yüklendi.")

                # Buradan sonrası mevcut dashboard.py'deki grafik ve tablo mantığı
                st.subheader("📄 Detaylı Sensör Verileri")
                st.dataframe(df, use_container_width=True)

                st.subheader("📈 Zaman Serisi Grafiği (EMG, Flex, Value)")
                # 'value' sütunu eksikse uyarı ver
                columns_to_plot = ["emg", "flex", "value"]
                available_columns = [col for col in columns_to_plot if col in df.columns]

                if available_columns:
                    # Altair ile daha esnek grafik çizimi
                    df_melted = df.melt(id_vars=["timestamp"], value_vars=available_columns, var_name="Sensor Type", value_name="Value")
                    chart = alt.Chart(df_melted).mark_line(point=True).encode(
                        x=alt.X("timestamp", title="Tarih ve Saat"),
                        y=alt.Y("Value", title="Sensör Değeri"),
                        color="Sensor Type:N",
                        tooltip=["timestamp", "Sensor Type", "Value"]
                    ).properties(
                        title="Sensör Verileri Zaman Serisi"
                    ).interactive() # Grafiği interaktif yap (yakınlaştırma, kaydırma)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("Grafik çizilecek sensör verisi (emg, flex, value) bulunamadı.")


            else:
                st.info("Henüz gösterilecek sensör verisi yok.")

        elif response.status_code == 401:
            st.error("Oturum süresi dolmuş olabilir, lütfen tekrar giriş yapın.")
            st.session_state.clear()
            st.query_params.update({"page": "login"})
            st.rerun()
            return
        else:
            st.error(f"Sensör verileri alınamadı. Hata kodu: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Sunucuya bağlanırken hata oluştu: {e}")
        st.info("Lütfen backend API'nizin çalıştığından emin olun.")



    # Aşağıdaki kodlar (eski örnek veri oluşturma ve grafikler) kaldırılabilir veya yorum satırına alınabilir
    # Eğer isterseniz, API'den veri gelmediğinde fallback olarak bu örnek verileri gösterebilirsiniz.
    # Ancak şimdilik bunları kaldırıyoruz ki kafa karışıklığı olmasın ve sadece API verisi kullanılsın.
    # --- ESKİ ÖRNEK VERİ OLUŞTURMA KODLARI BURADAN KALDIRILACAK ---
    # Örneğin şu kısımlar:
    # sensor_type = st.radio("Sensör Tipi Seç", ["EMG Kas Sensörü", "Flex Sensörleri"], horizontal=True)
    # ...
    # df = pd.DataFrame({
    #     "Tarih": dates,
    #     "Vücut Bölgesi": [body_part] * len(dates),
    #     "EMG (mV)": ...
    # })
    # ...
    # (veya mevcut mock verileri kullanmaya devam etmek isterseniz, API'den veri gelmediğinde gösterirsiniz)
