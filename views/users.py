from flask_restx import Resource, Namespace
from flask import request

from models import User, UserSchema
from setup_db import db
from views.required import admin_required, auth_required

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    @admin_required
    def get(self):
        data = db.session.query(User).all()
        users = UserSchema(many=True).dump(data)
        return users, 200

    def post(self):
        req_json = request.json
        user = User(**req_json)
        user.password = User.get_hash(user)

        db.session.add(user)
        db.session.commit()
        return "", 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @admin_required
    def get(self, uid):
        data = db.session.query(User).get(uid)
        user = UserSchema().dump(data)

        return user

    @auth_required
    def put(self, uid):
        user = db.session.query(User).get(uid)
        req_json = request.json
        user.username = req_json.get('username')
        user.password = User.get_hash(user)
        user.role = req_json.get('role')

        db.session.add(user)
        db.session.commit()

        return "", 204

    @auth_required
    def patch(self, uid):
        user = db.session.query(User).get(uid)
        req_json = request.json
        if 'username' in req_json:
            user.username = req_json.get('username')
        if 'password' in req_json:
            user.password = User.get_hash(user)
        if 'role' in req_json:
            user.role = req_json.get('role')

        db.session.add(user)
        db.session.commit()

        return "", 204

    @auth_required
    def delete(self, uid):
        user = db.session.query(User).get(uid)
        db.session.delete(user)
        db.session.commit()

        return "", 204
