import logging
from utils import error_msg
from flask_login import login_required
from flask import Blueprint, request, jsonify
from pymodm.errors import ValidationError

from db.models import Content
from utils import error_msg
from utils.login_utils import authorize, get_current_user
from utils.utils import get_timestamp
from utils.views_utils import ensure_not_exists


post_blueprint = Blueprint('post', __name__)
logger = logging.getLogger(__name__)

@post_blueprint.route('/content', methods=['POST'])
@login_required
@authorize({'admin'})
@ensure_not_exists(Content, 'title', 'title', error_msg.DUPLICATE_TITLE)
def create_post():
    try:
        post = Content(
            title = request.form['title'],
            content = request.form['content'],
            author = get_current_user().username,
            time = get_timestamp
        )
        post.save()
        return jsonify({
            'success': 1,
            'post_id': str(post._id)
        })
    except ValidationError as e:
        logger.warning(
            'Failed to create new slides. Exception: {}'.format(e.message)
        )
        return jsonify({
            'success': 0,
            'msg': '{} : {}'.format(error_msg.ILLEGAL_ARGUMENT, ','.join(list(e.message.keys())))
        }), 400


