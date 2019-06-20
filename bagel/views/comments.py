import logging
from flask import Blueprint, request, jsonify
from flask_login import login_required
from utils.login_utils import authorize
from utils import error_msg
from db.models import Comments, Content, User
from bson import ObjectId
from utils.login_utils import get_current_user
from pymodm.errors import ValidationError
from utils.views_utils import ensure_exists
from utils.utils import get_timestamp


comment_blueprint = Blueprint('comment', __name__)

logger = logging.getLogger(__name__)

@comment_blueprint.route('/create', methods=['POST'])
@login_required
@authorize({'admin', 'visitor'})
@ensure_exists(Content, 'post_id', '_id', error_msg.NO_POST_EXISTS, ObjectId)
def create_comment():
    try:
        comment = Comments(
            post_id = ObjectId(request.form['post_id']),
            comment = request.form['comment'],
            author_id = get_current_user()._id,
            author_name = get_current_user().username
        )
        comment.save()
        return jsonify({
            'success': 1,
            'comment_id': str(comment._id)
        })
    except ValidationError as e:
        logger.warning(
            'Failed to Create new comment. Exception: {}'.format(e.message)
        )
        return jsonify({
            'success': 0,
            'msg': '{}: {}'.format(error_msg.ILLEGAL_ARGUMENT, ','.join(list(e.message.keys())))
        }), 400

@comment_blueprint.route('/update', methods=['POST'])
@login_required
@authorize({'admin', 'visitor'})
@ensure_exists(Comments, 'comment_id', '_id', error_msg.NO_COMMENT_EXISTS, ObjectId)
def update_comment():
    comment_id = request.form['comment_id']
    comments = Comments.objects.get({'_id': ObjectId(comment_id)})
    comments.comment = request.form['comment']
    comments.save()
    return jsonify({
        'success': 1
    })

@comment_blueprint.route('/list_visitor', methods=['GET'])
@login_required
@authorize({'visitor'})
def list_visitor():
    user_id = get_current_user()._id
    post_id = request.args.get('post_id')
    logger.info('post_id: {}'.format(post_id))
    qs = Comments.objects.raw({'post_id': ObjectId(post_id)})
    logger.info('user_id: {}'.format(user_id))
    return jsonify({
        'success': 1,
        'msg': sorted([
            {
            'author_name': each.author_name,
            'comment': each.comment,
            'post_id': str(each.post_id._id),
            'permission': 1 if user_id == each.author_id._id else 0,
            'create_at': get_timestamp(each.create_at)
            } for each in qs
        ], key=lambda x: x['create_at'])
    })

@comment_blueprint.route('/list_admin', methods=['GET'])
@login_required
@authorize({'admin'})
def list_admin():
    post_id = request.args.get('post_id')
    qs = Comments.objects.raw({'post_id': ObjectId(post_id)})
    return jsonify({
        'success': 1,
        'msg': sorted(
            [{
                'comment': each.comment,
                'author_name': each.author_name,
                'post_id': str(each.post_id._id),
                'create_at': get_timestamp(each.create_at),
                'permission': 1
            } for each in qs],
            key = lambda x: x['create_at']
        )
    })


    



