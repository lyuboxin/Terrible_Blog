import logging
from utils import error_msg
from flask_login import login_required
from flask import Blueprint, request, jsonify
from pymodm.errors import ValidationError

from db.models import Content
from utils import error_msg
from utils.login_utils import authorize, get_current_user
from utils.utils import get_timestamp
from utils.views_utils import ensure_not_exists, ensure_exists

from bson import ObjectId


post_blueprint = Blueprint('post', __name__)
logger = logging.getLogger(__name__)

@post_blueprint.route('/create', methods=['POST'])
@login_required
@authorize({'admin'})
@ensure_not_exists(Content, 'title', 'title', error_msg.DUPLICATE_TITLE)
def create_post():
    try:
        post = Content(
            title = request.form['title'],
            content = request.form['content'],
            author = get_current_user().username,
            create_at = get_timestamp()
        )
        post.save()
        return jsonify({
            'success': 1,
            'post_id': str(post._id)
        })
    except ValidationError as e:
        logger.warning(
            'Failed to create new post. Exception: {}'.format(e.message)
        )
        return jsonify({
            'success': 0,
            'msg': '{} : {}'.format(error_msg.ILLEGAL_ARGUMENT, ','.join(list(e.message.keys())))
        }), 400

@post_blueprint.route('/delete', methods=['POST'])
@login_required
@authorize({'admin'})
@ensure_exists(Content, 'post_id', '_id', error_msg.NO_POST_EXISTS, ObjectId)
def delete_post():
    post_id = request.form['post_id']
    delete_post = Content.objects.get({'_id': ObjectId(post_id)})
    delete_post.delete()
    return jsonify({
        'success':1
    })

@post_blueprint.route('/update', methods=['POST'])
@login_required
@authorize({'admin'})
@ensure_exists(Content, 'post_id', '_id', error_msg.NO_POST_EXISTS, ObjectId)
def update_post():
    post_id = request.form['post_id']
    post = Content.objects.get({'_id': ObjectId(post_id)})
    post.title = request.form['title']
    post.content = request.form['content']
    post.save()
    return jsonify({
        'success': 1
    })

@post_blueprint.route('list', methods=['GET'])
@login_required
@authorize({'admin', 'visitor'})
def list_all():
    qs = Content.objects.all()
    return jsonify({
        'success': 1,
        'post': sorted([{
            'author': each.author,
            'title': each.title,
            'content': each.content,
            'create_at': get_timestamp(each.create_at)
        } for each in qs], key=lambda x: x['create_at'])
    })

@post_blueprint.route('/search_by_title', methods=['POST'])
@login_required
@authorize({'admin', 'visitor'})
def search_by_title():
    title = request.form['title']
    qs = Content.objects.raw({'title': {"$regex": title}})
    return jsonify({
        'success': 1,
        'msg': sorted([
            {
            'author': each.author,
            'title': each.title,
            'content': each.content,
            'create_at': get_timestamp(each.create_at)
            } for each in qs
        ], key=lambda x: x['create_at'])
    })

@post_blueprint.route('/search_by_author', methods=['POST'])
@login_required
@authorize({'admin', 'visitor'})
def search_by_author():
    username = request.form['username']
    qs = Content.objects.raw({'author':{'$regex': username}})
    return jsonify({
        'success': 1,
        'msg': sorted(
            [{
            'author': each.author,
            'title': each.title,
            'content': each.content,
            'create_at': get_timestamp(each.create_at)
            } for each in qs],
            key = lambda x: x['create_at']
        )
    })






