from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os
from flask_cors import CORS  # CORS import

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'defaultsecretkey')  # Secret key'i güvenli bir şekilde almak
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CORS izinlerini tüm uygulama için aç
CORS(app)

### MODELLER

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    emg = db.Column(db.Float)
    flex = db.Column(db.Float)
    value = db.Column(db.Float)

### TOKEN KONTROLÜ
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token eksik!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Geçersiz token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

### KULLANICI KAYIT
@app.route('/register_api', methods=['POST'])
def register_api():
    data = request.get_json()
    if not all(k in data for k in ('username', 'password')):
        return jsonify({'message': 'Eksik bilgi gönderildi!'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': f"Kullanıcı adı '{data['username']}' zaten alınmış!"}), 400  # Kullanıcı adı belirtildi

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Kullanıcı başarıyla oluşturuldu!'}), 201

### KULLANICI GİRİŞ
@app.route('/login_api', methods=['POST'])
def login_api():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Geçersiz kullanıcı adı veya şifre!'}), 401

    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token})

### SENSÖR VERİSİ EKLEME (KORUMALI)
@app.route('/sensor_data', methods=['POST'])
@token_required
def add_sensor_data(current_user):
    data = request.get_json()
    new_data = SensorData(
        user_id=current_user.id,
        emg=data.get('emg', 0),
        flex=data.get('flex', 0),
        value=data.get('value', 0)
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Sensör verisi başarıyla eklendi!'})

### SENSÖR VERİSİNİ GETİR (KORUMALI)
@app.route('/sensor_data', methods=['GET'])
@token_required
def get_sensor_data(current_user):
    datas = SensorData.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'emg': d.emg, 'flex': d.flex, 'value': d.value, 'timestamp': d.timestamp.isoformat()
    } for d in datas])

### SAĞLIK KONTROLÜ
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'API çalışıyor!'})

### SUNUCUYU BAŞLAT
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render için PORT env değişkeni
    app.run(host='0.0.0.0', port=port)


