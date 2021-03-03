"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#USER CRUD--------------------------------------------

@app.route('/user', methods=['GET'])
def get_user():
    user_query = User.query.all() 
    result = list(map(lambda x: x.serialize(), user_query)) #mapea y obtiene la data que viene en el array
    return jsonify(result), 200
@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first_or_404()
    return jsonify(user.serialize()), 200

   

@app.route('/user', methods=['POST']) #crea usuarios en la base de datos
def create_user():
    request_body = json.loads(request.data) #Peticion de los datos
    if request_body["email"] == None and request_body["password"] == None:
        return "Datos incompletos"
    else:
        user = User(email=request_body["email"], password=request_body["password"]) 
        db.session.add(user)
        db.session.commit()

        return "Successfully Created"
       

# People CRUD-------------------------------------

@app.route('/people', methods=['GET'])
def get_people():
    people_query = People.query.all()
    result = list(map(lambda x: x.serialize(), people_query)) #mapea el array de people
    return jsonify(result), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_people_by_id(id):
    people = People.query.filter_by(id=id).first_or_404()
    return jsonify(people.serialize()), 200

@app.route('/people', methods=['POST'])
def create_people():
    request_body = json.loads(request.data) #Peticion de los datos
    if request_body["name"] == None and request_body["hair_color"] == None and request_body["birthday"] == None and request_body["skin_color"]:
        return "Datos incompletos"
    else:
        people = People(name=request_body["name"], age=request_body["age"], hair_color=request_body["hair_color"], birthday=request_body["birthday"], skin_color=request_body["skin_color"], img=request_body["img"])
        db.session.add(people)
        db.session.commit()


        return "Successfully Created"

#FAVORITES CRUD-------------------------------------------

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favs_query = Favorites.query.all()
    result = list(map(lambda x: x.serialize(), favs_query))
    return jsonify(result), 200
@app.route('/favorites/<int:id>', methods=['GET'])
def get_fav_by_id(id):
    fav = Favorites.query.filter_by(id=id).first_or_404()
    return jsonify(fav.serialize()), 200

# @app.route('/favorites', methods=['POST'])
# def create_favs():
#     request_body = json.loads(request.data)
#     if request_body["name"] == None and request_body["favorites_user"] == None:
#         return "Datos incompletos"
#     else:
#         fav = Favorites(name="name"), Favorites(favorites_user="favorites_user")
#         return request_body, 200

#PLANETS CRUD------------------------------------------------
@app.route('/planets', methods=['GET'])
def get_planets():
    planets_query = Planets.query.all()
    result = list(map(lambda x: x.serialize(), planets_query))
    return jsonify(result), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    planet = Planets.query.filter_by(id=id).first_or_404()
    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def create_planet():
    request_body = json.loads(request.data) #Peticion de los datos
    if request_body["name"] == None and request_body["weather"] == None and request_body["diameter"] == None and request_body["orbital"] and request_body["img"] == None:
        return "Datos incompletos"
    else:
        planet = Planets(name=request_body["name"], weather=request_body["weather"], diameter=request_body["diameter"], orbital=request_body["orbital"], img=request_body["img"])
        db.session.add(planet)
        db.session.commit()


        return "Successfully Created"







# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
