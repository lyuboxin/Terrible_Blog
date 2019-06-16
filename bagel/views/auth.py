import logging
from utils import login_utils
from flask import Blueprint, jsonify, request
from db.models import User, VerificationCode
from flask_login import login_user
from utils import email_utils, error_msg, utils
from pymodm.errors import ValidationError


auth_blueprint = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

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

@auth_blueprint.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    email = request.form['email']
    try:
        user = User.objects.get({'email':email})
    except:
        return jsonify({
            'success':0,
            'msg': error_msg.USER_NOT_EXISTS
        }),404

    # prev = VerificationCode.objects.raw({"user_id"})
    # prev.delete()

    code = utils.random_string(6)
    new_code = VerificationCode(
        user_id = user._id,
        code = code
    )

    try:
        new_code.save()
    except ValidationError as e:
        logger.warning(
            'Failed to create new verification code. Exception: {}'.format(e.message))
        return jsonify({
            'success': 0,
            'msg': '{}: {}'.format(error_msg.ILLEGAL_ARGUMENT, ','.join(list(e.message.keys())))
        }), 400

    logger.info('Send verification code to {}'.format(user.email))
    email_utils.send(
        email,
        "verification code for reset password",
        "verfication code: {}".format(code)
    )

    return jsonify({
        'success': 1
    })

@auth_blueprint.route('/verify_code', methods=['POST'])
def verify_code():
    email = request.form['email']
    code = request.form['code']
    try:
        user = User.objects.get({'email': email})
    except:
        return jsonify({
            'success': 0,
            'msg': error_msg.USER_NOT_EXISTS
        }), 404
    vcode = VerificationCode.objects.raw({'user_id': user._id})
    if vcode.count() == 0 or vcode.first().code != code:
        return jsonify({
            "success": 0
        })
    return jsonify({
        "success": 1
    })

@auth_blueprint.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form['email']
    code = request.form['code']
    new_password = request.form['password']
    try:
        user = User.objects.get({'email': email})
    except:
        return jsonify({
            'success': 0,
            'msg': error_msg.USER_NOT_EXISTS
        }), 404
    vcode = VerificationCode.objects.raw({'user_id': user._id})
    if vcode.count() == 0 or vcode.first().code != code:
        return jsonify({
            'success': 0
        })
    
    try:
        user.password = new_password
        user.save()
    except ValidationError as e:
        return jsonify({
            'success': 0,
            'msg': '{}:{}'.format(error_msg.ILLEGAL_ARGUMENT, ','.join(list(error_msg.keys())))
        }), 400
    return jsonify({
        'success': 1
    })



    
