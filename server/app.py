#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return make_response({ "message": "Welcome to the Super Hero page!" }, 200)

api.add_resource(Home, '/')

class Heroes(Resource):
    def get(self):
        hero_dicts = [hero.to_dict(rules=('-hero_powers',)) for hero in Hero.query.all()]

        return make_response(
            jsonify(hero_dicts),
            200
        )
    
api.add_resource(Heroes, '/heroes')

class HeroById(Resource):
    def get(self, id):
        hero = Hero.query.filter(Hero.id == id).first()
        
        if not hero:
            return make_response({ "error": "Hero not found" }, 404)
        
        hero_dict = hero.to_dict(rules=('powers',))

        return make_response(
            jsonify(hero_dict),
            200
        )
    
api.add_resource(HeroById, '/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        power_dicts = [power.to_dict(rules=('-hero_powers',)) for power in Power.query.all()]

        return make_response(
            jsonify(power_dicts),
            200
        )
    
api.add_resource(Powers, '/powers')

class PowerById(Resource):
    def get(self, id):
        power = Power.query.filter(Power.id == id).first()
        
        if not power:
            return make_response({
                "error": "Power not found"
            }, 404)
        
        power_dict = power.to_dict(rules=('heroes',))

        return make_response(
            jsonify(power_dict),
            200
        )
    
    def patch(self, id):
        power = Power.query.filter(Power.id == id).first()
        data = request.get_json()

        if not power:
            return make_response({
                "error": "Power not found"
            }, 404)
        try:
            for attr in data:
                setattr(power, attr, request.get_json()[attr])

            db.session.add(power)
            db.session.commit()

            power_dict = power.to_dict(rules=('heroes',))

            return make_response(
                jsonify(power_dict),
                200
            )

        except Exception as e:
            return make_response({ "error": "Invalid input" }, 400)

api.add_resource(PowerById, '/powers/<int:id>')

class HeroPowers(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_hero_power = HeroPower(
                strength=data['strength'],
                hero_id=data['hero_id'],
                power_id=data['power_id']
            )

            db.session.add(new_hero_power)
            db.session.commit()

            hero_power_dict = new_hero_power.hero.to_dict(rules=('hero_powers',))

            return make_response(
                jsonify(hero_power_dict),
                201
            )

        except:
            return make_response({ "error": "Invalid input" }, 400)

api.add_resource(HeroPowers, '/hero_powers')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

# from flask import Flask, request, make_response, jsonify
# from flask_cors import CORS
# from flask_migrate import Migrate
# from flask_restful import Api, Resource

# from models import db, Hero, Power, HeroPower

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# CORS(app)
# migrate = Migrate(app, db)

# db.init_app(app)

# api = Api(app)

# @app.route('/')
# def home():
#     return ''

# class Hero(Resource):
#     def get(self):
#         heroes = Hero.query.all()
#         heroes_dict_list = [hero.to_dict() for hero in heroes]
#         response = make_response(heroes_dict_list, 200)
#         return response

# class HeroById(Resource):
#     def get(self, id):
#         hero = Hero.query.filter(Hero.id == id).first()
#         if not hero:
#             return make_response({
#                 "error": "Hero not found"
#             }, 404)
#         response = make_response(hero.to_dict(rules=('powers',)), 200)
#         return response

# class Power(Resource):
#     def get(self):
#         powers = Power.query.all()
#         powers_dict_list = [power.to_dict() for power in powers]
#         response = make_response(powers_dict_list, 200)
#         return response

# class PowerById(Resource):
#     def get(self, id):
#         power = Power.query.filter(Power.id == id).first()
#         if not power:
#             return make_response({
#                 "error": "Power not found"
#             }, 404)
#         response = make_response(power.to_dict(), 200)
#         return response
    
#     def patch(self, id):
#         data = request.get_json()

#         power = Power.query.filter_by(id=id).first()
#         description = power.description
        # if not power:
        #     return make_response({
        #         "error": "Power not found"
        #     }, 404)
#         try:
#             for attr in data:
#                 setattr(description, attr, request.form[attr])
        
#             db.session.add(description)
#             db.session.commit()
#         except Exception as e:
#             response_dict = {
#                 "errors": "Invalid Input"
#             }
#             return make_response(
#                 response_dict,
#                 422
#             )
#         response = make_response(description.to_dict(), 200)

#         return response

# class HeroPowers(Resource):
#     def post(self):
#         data = request.get_json()
#         try:
#             hero_powers = HeroPower(
#                 strength=data["strength"],
#                 power_id=data["power_id"],
#                 hero_id=data["hero_id"]
#             )
#             db.session.add(hero_powers)
#             db.session.commit()
#         except Exception as e:
#             response_dict = {
#                 "errors": "Invalid Input"
#             }
#             return make_response(
#                 response_dict,
#                 422
#             )
#         response = make_response(
#             hero_powers.hero.to_dict(),
#             201
#         )
#         return response

# api.add_resource(Hero, '/heroes')
# api.add_resource(HeroById, '/heroes/<int:id>')
# api.add_resource(Power, '/powers')
# api.add_resource(PowerById, '/powers/<int:id>')
# api.add_resource(HeroPowers, '/hero_powers')

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)
