#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)


class PlantByID(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)  
        if not plant:
            return {"error": "Plant not found"}, 404
        return plant.to_dict(), 200

    def patch(self, id):
        plant = db.session.get(Plant, id)   
        if not plant:
            return {"error": "Plant not found"}, 404

        data = request.get_json()
        for attr, value in data.items():
            setattr(plant, attr, value)

        db.session.commit()
        return plant.to_dict(), 200

    def delete(self, id):
        plant = db.session.get(Plant, id)   
        if not plant:
            return {"error": "Plant not found"}, 404

        db.session.delete(plant)
        db.session.commit()
        return {}, 204


api.add_resource(PlantByID, "/plants/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)




