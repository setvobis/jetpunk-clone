from datetime import datetime
from jetskunk import db, login_m
from flask_login import UserMixin


@login_m.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(30), unique=True, nullable=False)
    email = db.Column(db.Text(120), unique=True, nullable=False)
    password = db.Column(db.Text(60), nullable=False)
    quiz_created = db.relationship('Quiz', backref='creator', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(150), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Quiz('{self.title}', '{self.date_created}')"
