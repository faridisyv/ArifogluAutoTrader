from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Association table for User favorites
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('car_id', db.Integer, db.ForeignKey('car.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    profile_photo = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='buyer') # buyer, seller
    # Relationships
    cars = db.relationship('Car', backref='seller', lazy=True)
    favorite_cars = db.relationship('Car', secondary=favorites, lazy='subquery',
        backref=db.backref('favorited_by', lazy=True))

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.String(50))
    transmission = db.Column(db.String(50))
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relationships
    images = db.relationship('Image', backref='car', lazy=True, cascade="all, delete-orphan")

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
