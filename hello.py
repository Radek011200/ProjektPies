import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
current_path = os.path.abspath(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_path, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


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