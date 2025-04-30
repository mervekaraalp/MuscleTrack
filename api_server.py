from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Veritabanı Modelleri
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    emg = db.Column(db.Float)
    flex = db.Column(db.Float)
    value = db.Column(db.Float)

# Kullanıcı kayıt API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Kayıt başarılı!'})

# Kullanıcı giriş API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Hatalı kullanıcı adı veya şifre!'}), 401
    return jsonify({'message': 'Giriş başarılı!', 'user_id': user.id})

# Sensor verisi ekleme API
@app.route('/sensor_data', methods=['POST'])
def add_sensor_data():
    data = request.get_json()
    new_data = SensorData(
        user_id=data['user_id'],
        emg=data['emg'],
        flex=data['flex'],
        value=data['value']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Sensor verisi kaydedildi!'})

with app.app_context():
    db.create_all()

