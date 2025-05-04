import streamlit as st
import requests

# Flask API'nin URL'si
API_URL = "https://muscletrack.onrender.com"

# Kullanıcıdan token al
def get_token():
    token = st.text_input("Lütfen giriş yapın (Token'ınızı girin):")
    return token

# Sensör verilerini almak için GET isteği
def get_sensor_data(token):
    headers = {'x-access-token': token}  # Token'ı header'a ekliyoruz
    response = requests.get(f"{API_URL}/sensor_data", headers=headers)
    if response.status_code == 200:
        return response.json()  # Veri başarıyla alındığında JSON formatında döner
    else:
        st.error("Veri alınamadı!")
        return None

# Sensör verisini eklemek için POST isteği
def send_sensor_data(token, emg, flex, value):
    headers = {'x-access-token': token}  # Token'ı header'a ekliyoruz
    payload = {'emg': emg, 'flex': flex, 'value': value}  # Sensör verisini gönderiyoruz
    response = requests.post(f"{API_URL}/sensor_data", json=payload, headers=headers)
    if response.status_code == 200:
        st.success("Sensör verisi başarıyla eklendi!")
    else:
        st.error("Veri eklenemedi!")

# Başlangıç sayfası
st.set_page_config(page_title="MuscleTrack", page_icon="💪", layout="centered")

st.title("💪 MuscleTrack'e Hoş Geldin!")
st.markdown(
    """
    ### Kas aktiviteni takip etmeye hazır mısın?
    👈 Sol menüden ilgili sayfaları seçerek egzersiz geçmişine ulaşabilir, kas verilerini inceleyebilir ve yapay zeka destekli öneriler alabilirsin.
    
    ---
    """
)

st.image("https://media.giphy.com/media/26ufnwz3wDUli7GU0/giphy.gif", caption="Haydi Başlayalım!", use_container_width=True)

# Giriş Kontrolü
token = get_token()
if token:
    st.success("Başarıyla giriş yapıldı!")
    
    # Kullanıcıyı bilgilendiren mesaj
    st.markdown("### Sensör Verilerinizi Gönderin veya Görüntüleyin")

    # Veri gönderme kısmı
    st.subheader("Yeni Sensör Verisi Ekle")
    emg = st.number_input("EMG Değeri", min_value=0.0, step=0.1)
    flex = st.number_input("Flex Değeri", min_value=0.0, step=0.1)
    value = st.number_input("Değer", min_value=0.0, step=0.1)

    if st.button("Sensör Verisini Gönder"):
        if emg and flex and value:
            send_sensor_data(token, emg, flex, value)

    # Sensör verilerini görüntüleme kısmı
    st.subheader("Sensör Verilerini Görüntüle")
    data = get_sensor_data(token)
    if data:
        for entry in data:
            st.write(f"Zaman: {entry['timestamp']}, EMG: {entry['emg']}, Flex: {entry['flex']}, Değer: {entry['value']}")

else:
    st.warning("Lütfen giriş yapınız!")

