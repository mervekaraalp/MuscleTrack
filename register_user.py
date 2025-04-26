import requests

# API endpoint ve kullanıcı verileri
url = "http://127.0.0.1:5000/register"  # API'nin doğru URL'sini kullandığınızdan emin olun
user_data = {
    "username": "newuser",  # Yeni kullanıcı adı
    "password": "password123"  # Kullanıcı şifresi
}

# POST isteğini gönderme
response = requests.post(url, json=user_data)

# Yanıtın durum kodunu kontrol et
if response.status_code == 200:
    try:
        # JSON formatında yanıtı çözümle
        print("Başarılı: ", response.json())
    except ValueError:
        print("Yanıt JSON formatında değil:", response.text)
else:
    print(f"İstek başarısız oldu, durum kodu: {response.status_code}")
    print("Yanıt:", response.text)

