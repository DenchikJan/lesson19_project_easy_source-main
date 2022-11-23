from flask_restx import Resource, Namespace
from flask import request

from views.required import auth_required, admin_required
from models import Director, DirectorSchema
from setup_db import db

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        director = Director(**req_json)

        db.session.add(director)
        db.session.commit()
        return "", 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        r = db.session.query(Director).get(rid)
        req_json = request.json

        r.name = req_json.get('name')

        db.session.add(r)
        db.session.commit()
        return "", 204

    @admin_required
    def delete(self, rid):
        r = db.session.query(Director).get(rid)

        db.session.delete(r)
        db.session.commit()
        return "", 204
