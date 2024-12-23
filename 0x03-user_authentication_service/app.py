#!/usr/bin/env python3
"""BAsic flask app"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def home():
    """ return a JSON payload of the form"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """POST route to register a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registerd"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Creates a new session for the user."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if session_id:
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Log out"""
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        abort(403)

    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except NoResultFound:
        abort(403)


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile():
    """Find a user and display it's profile"""
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        abort(403)

    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user is None:
            abort(403)
        return jsonify({"email": user.email}), 200
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Gets reset password token"""
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Update password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    message = {"email": email, "message": "Password updated"}
    return jsonify(message), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
