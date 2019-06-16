from flask import Blueprint, jsonify, request
from db.models import User, AdminCode
from utils import error_msg, views_utils, login_utils
from db import dbutils
import logging
from pymodm.errors import ValidationError

user_blueprint = Blueprint('user', __name__)
logger = logging.getLogger(__name__)

@user_blueprint.route('/register', methods=['POST'])
@views_utils.ensure_not_exists(User, 'username', 'username', error_msg.DUPLICATE_USERNAME)
def register():
    try:
        username = request.form['username']
        logger.info("username:{}".format(username))
        new_user = User(
            username = username,
            password = request.form['password'],
            email = request.form['email'],
            type = 'visitor',
            code = 0
        )
        new_user.save()
    except ValidationError as e:
        logger.warning(
            'Failed to create new user. Exception: {}'.format(e.message)
        )
        return jsonify({
            'success': 0,
            'msg': '{}:{}'.format(error_msg.ILLEGAL_ARGUMENT,','.join(list(e.message.keys())))
        }), 400

    logger.info('Created new user: {}'.format(username))
    return jsonify({'success': 1})


@user_blueprint.route('/admin_register', methods=['POST'])
@views_utils.ensure_not_exists(User, 'username', 'username', error_msg.DUPLICATE_USERNAME)
def admin_register():
    try:
        code = request.form['code']
        code_verify = AdminCode.objects.get({'code': code})
        logger.info("code_verify: {}".format(code))
    except:
        return jsonify({
            "success": 0,
            "msg": "code is wrong"
        })
    try:
        username = request.form['username']
        new_admin = User(
            username = username,
            password = request.form['password'],
            email = request.form['email'],
            type = 'admin',
            code = request.form['code']
        )
        new_admin.save()
    except ValidationError as e:
        logger.warning(
            'Failed to create new user, Exception: {}'.format(e.message)
        )
        return jsonify({
            'success': 0,
            'msg': '{}:{}'.format(error_msg.ILLEGAL_ARGUMENT, ','.join(list(e.message.keys())))
        }),400
    logger.info('Created new admin: {}'.format(username))
    return jsonify({
        'success': 1
    })





