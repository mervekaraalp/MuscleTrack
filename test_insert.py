# test_insert.py
from app import app, db, SensorData, User
from datetime import datetime

# Uygulama bağlamı oluştur
with app.app_context():
    # Bir kullanıcı seç (örnek olarak "mervekaraalp")
    user = User.query.filter_by(username="mervekaraalp").first()

    if user:
        # SensorData modeline yeni veri eklemek
        new_data = SensorData(
            user_id=user.id,  # Kullanıcı ID'si
            timestamp=datetime.now(),  # Şu anki zaman
            value=42.5  # Örnek sensör verisi
        )
        
        # Yeni veriyi veritabanına ekle
        db.session.add(new_data)
        db.session.commit()  # Değişiklikleri kaydet
        
        print("Veri başarıyla eklendi.")
    else:
        print("Kullanıcı bulunamadı.")
