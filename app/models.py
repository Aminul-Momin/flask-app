import datetime
from flask_login import UserMixin
import jwt
#==============================================================================
from app import db, login_manager, app
#==============================================================================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')


    def get_reset_token(self, expires_sec=1800):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=expires_sec),
            'iat': datetime.datetime.utcnow(),
            'sub': self.id
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        try: user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')['sub']
        except: return None # invalid token
        return User.query.get(user_id)

    def __repr__(self):
        return f"{self.username}, {self.email}"

class Post(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"{self.title}, {self.date_posted}"