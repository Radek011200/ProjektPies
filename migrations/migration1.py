from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,
    primary_key=True)
    name = db.Column(db.String(64),
    unique=True)
    users = db.relationship('User',
    backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
    primary_key=True)
    username = db.Column(db.String(64),
    unique=True, index=True)
    role_id = db.Column(db.Integer,
    db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username
    
class Dog(db.Model):
    __tablename__ = 'dog',
    id = db.Column(db.Integer,
        primary_key=True)
    name = db.Column(db.String(64),
        nullable=False)
    age = db.Column(db.Integer,
        nullable=False)
    breed = db.Column(db.String(64),
        )
    photo = db.Column(db.String(100))

    def __init__(self, name, age, breed="mongrel", photo=None):
        self.name = name
        self.age = age
        self.breed = breed
        self.photo = photo