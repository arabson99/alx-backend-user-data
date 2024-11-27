#!/usr/bin/env python3

""" Module of Session authentication views"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """" Auth session login"""
    email = request.form.get('email')
    if not email:
        return make_response(jsonify({"error": "email missing"}), 400)

    password = request.form.get('password')
    if not password:
        return make_response(jsonify({"error": "password missing"}), 400)

    try:
        users = User.search({"email": email})
    except Exception as e:
        return make_response(jsonify({"error": "server error"}), 500)

    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    from api.v1.app import auth
    for user in users:
        if user.is_valid_password(password):
            session_id = auth.create_session(user.id)
            session_name = getenv('SESSION_NAME')
            respose = make_response(user.to_json())
            respose.set_cookie(session_name, session_id)
            return respose

    return make_response(jsonify({"error": "wrong password"}), 401)


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ Auth session logou.t"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
