"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200





@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    people_dictionary = []
    for person in people:
        people_dictionary.append(person.serialize())

    return jsonify(people_dictionary), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)

    return jsonify(person.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planet_dictionary = []
    for planet in planets:
        planet_dictionary.append(planet.serialize())

    return jsonify(planet_dictionary), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planets = Planet.query.get(planet_id)

    return jsonify(planets.serialize()), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_dictionary = []
    for user in users:
        users_dictionary.append(user.serialize())

    return jsonify(users_dictionary), 200


@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    favorites_dictionary = []
    for favorite in favorites:
        favorites_dictionary.append(favorite.serialize())

    return jsonify(favorites_dictionary), 200


@app.route('/<users>/favorites', methods=['POST'])
def post_favorite(users):

    body = request.json
    favorite = Favorite(name=body["name"], link=body["link"], user_id=users)
    db.session.add(favorite)
    db.session.commit()

    return "worked", 200


@app.route('/<users>/favorites', methods=['GET'])
def get_user_favorites(users):

    favorites = Favorite.query.filter_by(user_id=users)
    favorites_dictionary = []
    for favorite in favorites:
        favorites_dictionary.append(favorite.serialize())
    return "worked", 200


@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):

    favorite = db.session.get(Favorite, favorite_id)
    db.session.delete(favorite)
    db.session.commit()
    return "worked", 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
