from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_migrate import Migrate

# Flask ve veritabanı ayarlarını yapalım
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///muscletrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

# Veritabanı ve Migrate başlatıyoruz
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Token doğrulama decorator'ı
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()
        except Exception as e:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Kullanıcı kaydı
@app.route('/register_api', methods=['POST'])
def register_api():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

# Giriş ve token üretimi
@app.route('/login_api', methods=['POST'])
def login_api():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token})

# Sensör verisi
@app.route('/sensor_data', methods=['GET'])
@token_required
def sensor_data(current_user):
    user_data = SensorData.query.filter_by(user_id=current_user.id).all()
    result = []
    for data in user_data:
        result.append({
            'timestamp': data.timestamp,
            'emg': data.emg,
            'flex': data.flex,
            'value': data.value
        })
    return jsonify({'sensor_data': result})

# Kullanıcı ayarları - Get Settings
@app.route('/get_settings', methods=['GET'])
@token_required
def get_settings(current_user):
    settings = Settings.query.filter_by(user_id=current_user.id).first()
    if not settings:
        settings = Settings(user_id=current_user.id)
        db.session.add(settings)
        db.session.commit()
    
    return jsonify({
        'preferred_language': settings.preferred_language,
        'theme': settings.theme,
        'graph_type': settings.graph_type,
        'notification_enabled': settings.notification_enabled
    })

# Kullanıcı ayarları - Update Settings
@app.route('/update_settings', methods=['PUT'])
@token_required
def update_settings(current_user):
    data = request.get_json()
    settings = Settings.query.filter_by(user_id=current_user.id).first()

    if not settings:
        settings = Settings(user_id=current_user.id)

    settings.preferred_language = data.get('preferred_language', settings.preferred_language)
    settings.theme = data.get('theme', settings.theme)
    settings.graph_type = data.get('graph_type', settings.graph_type)
    settings.notification_enabled = data.get('notification_enabled', settings.notification_enabled)

    db.session.add(settings)
    db.session.commit()

    return jsonify({'message': 'Settings updated successfully!'})

# Kullanıcı güncelleme
@app.route('/update_user', methods=['PUT'])
@token_required
def update_user(current_user):
    data = request.get_json()
    if not check_password_hash(current_user.password, data['current_password']):
        return jsonify({'message': 'Current password is incorrect!'}), 401

    if data.get('username'):
        current_user.username = data['username']
    if data.get('password'):
        current_user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    db.session.commit()
    return jsonify({'message': 'User updated successfully!'}), 200

# Veritabanı tabloları oluşturuluyor
with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)


# Veritabanı modelleri
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    settings = db.relationship('Settings', backref='user', uselist=False)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    preferred_language = db.Column(db.String(10), default='tr')
    theme = db.Column(db.String(10), default='light')
    graph_type = db.Column(db.String(20), default='line')
    notification_enabled = db.Column(db.Boolean, default=True)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    emg = db.Column(db.Float)
    flex = db.Column(db.Float)
    value = db.Column(db.Float)

