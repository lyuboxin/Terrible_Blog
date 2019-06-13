import logging
from utils import login_utils
from flask import Blueprint, jsonify, request
from db.models import User
from flask_login import login_user

auth_blueprint = Blueprint('auth', __name__)
logging = logging.getLogger(__name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        user = User.objects.get({'username': username, 'password': password})
    except:
        return jsonify({
            'success': 0,
        })

    u = login_utils.UserLogin()
    u.id = user._id
    login_user(u)
    return jsonify({
        'success': 1
    })