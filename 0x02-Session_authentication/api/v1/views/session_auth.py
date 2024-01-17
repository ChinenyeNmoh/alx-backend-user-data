#!/usr/bin/env python3
""" Module of session auth views
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
    - email
    - password
    Return:
    - User object JSON represented
    - 400 if email or password is missing or empty
    - 404 if no User found
    - 401 if the password is not the one of the user found
    """
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    
    if not user_email:
        return jsonify({"error": "email missing"}), 400
    if not user_password:
        return jsonify({"error": "password missing"}), 400
    
    user_list = User.search({'email': user_email})
    
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404
    
    for user in user_list:
        if user.is_valid_password(user_password):
            from api.v1.app import auth
            user_id = user.id
            session_id = auth.create_session(user_id)
            session_user_json = jsonify(user.to_json())
            session_user_json.set_cookie(getenv('SESSION_NAME'), session_id)
            return session_user_json
        else:
            return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Delete route"""
    from api.v1.app import auth
    is_delete = auth.destroy_session(request)
    if is_delete:
        return jsonify({}), 200
    else:
        abort(404)
