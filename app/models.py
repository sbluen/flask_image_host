from datetime import datetime

from flask_login import UserMixin

from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    images = db.relationship(
        "Image", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    api_keys = db.relationship(
        "ApiKey", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<User {self.username}>"


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<Image {self.filename}>"


class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<ApiKey {self.key[:8]}...>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
