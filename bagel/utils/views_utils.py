import logging
from flask import request, jsonify
from utils import error_msg
from functools import wraps

from db import dbutils

logger = logging.getLogger(__name__)

def get_val_from_req(field_name):
    if request.method == 'GET':
        field = request.args.get(field_name)
    else:
        field = request.form[field_name]
    return field

def _req_field_exists_in_db(model, field_name, field_name_in_db, field_type):
    field = get_val_from_req(field_name)
    logger.info('_id:{}'.format(field))
    logger.info('post_id :{}'.format(field_name))
    if not field_type:
        res = dbutils.exists(model, {field_name_in_db: field})
    else:
        res = dbutils.exists(model, {field_name_in_db: field_type(field)})
    logger.debug('Checking if {}:{}:{} exists: {}'.format(
        model.__name__, field_name_in_db, field, res))
    return res

def ensure_exists(model, field_name, field_name_in_db, error_msg, field_type=None):
    def wrapper(f):
        @wraps(f)
        def check():
            if _req_field_exists_in_db(model, field_name, field_name_in_db if field_name_in_db else field_name, field_type):
                return f()
            else:
                return jsonify({
                    'success': 0,
                    'msg': error_msg
                }), 404
        return check
    return wrapper

def ensure_not_exists(model, field_name, field_name_in_db, error_msg, field_type=None):
    def wrapper(f):
        @wraps(f)
        def check():
            if not _req_field_exists_in_db(model, field_name, field_name_in_db if field_name_in_db else field_name, field_type):
                return f()
            else:
                return jsonify({
                    'success': 0,
                    'msg': error_msg
                }), 409
        return check
    return wrapper
