import os
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

current_path = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_path, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dogs', methods=['GET', 'POST'])
def dogs():
    return render_template('dogs.html', dogs = Dog.query.all())

@app.route('/create', methods=['GET', 'POST'])
def create():
    name = None
    form = NameForm()
    if form.validate_on_submit():

        photo = form.photo.data
        filename = secure_filename(photo.filename)
        if(filename):
            photo.save('static/' + filename)

        dog = Dog(
            name = request.form.get('name'),
            breed = request.form.get('breed'),
            age = request.form.get('age'),
            photo = filename if filename is not None else photo)

        db.session.add(dog)
        db.session.commit()
        flash('Dodano pieska')

        return redirect(url_for('dogs'))
    return render_template('create.html', form=form, name=session.get('name'))

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    dog = Dog.query.get(id)

    if dog is None:
        return render_template('404.html'), 404
    form = NameForm(
        name = dog.name,
        breed = dog.breed,
        age = dog.age,
        )

    if request.method == 'POST':
        if form.validate_on_submit():

            photo = form.photo.data
            filename = None
            if not isinstance(photo, str):
                filename = secure_filename(photo.filename)
                photo.save('static/' + filename)


            dog.name = request.form.get('name')
            dog.breed = request.form.get('breed')
            dog.age = request.form.get('age')
            dog.photo = filename if filename is not None else photo

            db.session.add(dog)
            db.session.commit()
            flash('Edytowano pieska')

            return redirect(url_for('dogs'))
    return render_template('edit.html', dog=dog, form=form)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route("/dog/<id>")
def dog_delete(id):
    dog = Dog.query.get(id)
    db.session.delete(dog)
    db.session.commit()

    flash('Usunięto pieska')

    return redirect(url_for('dogs'))

@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class NameForm(FlaskForm):
    name = StringField('Imie', validators=[DataRequired()])
    breed = StringField('Rasa', validators=[DataRequired()])
    age = IntegerField('Wiek', validators=[DataRequired()])
    photo = FileField('Zdjecie')
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
    __tablename__ = 'dog'
    id = db.Column(db.Integer,
        primary_key=True)
    name = db.Column(db.String(64),
        nullable=False)
    age = db.Column(db.Integer)
    breed = db.Column(db.String(64),
        )
    photo = db.Column(db.String(100))

    def __init__(self, name, age, breed="mongrel", photo=None):
        self.name = name
        self.age = age
        self.breed = breed
        self.photo = photo

if __name__ == '__main__':
    app.run()