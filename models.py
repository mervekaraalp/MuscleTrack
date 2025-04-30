
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Ayarlar ilişkisi
    settings = db.relationship('Settings', backref='user', uselist=False)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    preferred_language = db.Column(db.String(10), default='tr')
    theme = db.Column(db.String(10), default='light')  # light / dark
    graph_type = db.Column(db.String(20), default='line')  # line / bar / area
    notification_enabled = db.Column(db.Boolean, default=True)

# Eğer SensorData kullanmak istiyorsan:
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('sensor_data', lazy=True))
