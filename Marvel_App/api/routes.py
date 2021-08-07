from flask import Blueprint
from flask import request, jsonify
from Marvel_App.helpers import token_required
from Marvel_App.models import db, User, Hero, hero_schema, heroes_schema

api = Blueprint('api',__name__,url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}

@api.route('/heroes', methods=['POST'])
@token_required
def create_hero(current_user_token):
    name = request.json['name']
    description = request.json['description']
    superpower = request.json['superpower']
    user_token = current_user_token.token
    print(f'TESTER: {current_user_token.token}')

    hero = Hero(name, description, superpower, user_token = user_token)

    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)

@api.route('/heroes', methods=['GET'])
@token_required
def get_heroes(current_user_token):
    owner = current_user_token.token
    heroes = Hero.query.filter_by(user_token = owner).all()
    response = heroes_schema.dump(heroes)
    return jsonify(response)

@api.route('/heroes/<id>', methods = ['GET'])
@token_required
def get_hero(current_user_token, id):
    hero = Hero.query.get(id)
    response = hero_schema.dump(hero)
    return jsonify(response)

@api.route('/heroes/<id>', methods = ['POST'])
@token_required
def update_drone(current_user_token, id):
    hero = Hero.query.get(id)
    print(hero)
    if hero:
        hero.name = request.json['name']
        hero.description = request.json['description']
        hero.superpower = request.json['superpower']
        hero.user_token = current_user_token.token
        db.session.commit()
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That drone does not exist!'})

@api.route('/heroes/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    if hero:
        db.session.delete(hero)
        db.session.commit()

        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That drone does not exist!'})

