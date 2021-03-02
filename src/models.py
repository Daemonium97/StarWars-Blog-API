from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    
    # Here we define db.Columns for the table address.
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    
    favorites_user = db.Column(db.Integer, db.ForeignKey(User.id))

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            
            "favorites_user": self.favorites_user
        }


class People(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(250))
    birthday = db.Column(db.Integer)
    skin_color = db.Column(db.String(250))
    img = db.Column(db.String(250))

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "age": self.name,
            "hair_color": self.hair_color,
            "birthday": self.birthday,
            "skin_color": self.skin_color,
            "img": self.img
        }

class Planets(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    weather = db.Column(db.String(250))
    diameter = db.Column(db.Integer)
    orbital = db.Column(db.Integer)
    img = db.Column(db.String(250))

    def serialize(self):
        return{
        "id": self.id,
        "name": self.name,
        "weather": self.weather,
        "diameter": self.diameter,
        "orbital": self.orbital,
        "img": self.img 
        }
       
