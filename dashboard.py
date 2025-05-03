import streamlit as st
import requests
import pandas as pd

st.title("MuscleTrack Dashboard")

if "token" not in st.session_state:
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

token = st.session_state["token"]
username = st.session_state["username"]

st.success(f"Hoş geldin, {username}!")

headers = {"x-access-token": token}
response = requests.get("http://localhost:5000/sensor_data", headers=headers)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)

    st.line_chart(df.set_index("timestamp")[["emg", "flex", "value"]])
else:
    st.error("Veri alınamadı. Token süresi dolmuş olabilir.")

