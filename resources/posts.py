from flask import abort, jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc
from middlewares import auth_required, developer_required
from schemas.filters import FiltersQueryArgsSchema
from schemas.post import PostsListSchema, PostSchema, PostsCreateSchema, PostsUpdateSchema
from models.post import Post

posts = Blueprint('posts', 'posts', url_prefix='/posts')


@posts.route('/')
class Posts(MethodView):
    @posts.arguments(FiltersQueryArgsSchema, location='query')
    @posts.response(200, PostsListSchema)
    def get(self, arguments):
        query = Post.query.filter_by(deleted=False)
        count = query.count()

        query = query.order_by(desc('created_at'))

        return {
            'posts': query.all(),
            'count': count
        }

    @auth_required
    @developer_required
    @posts.arguments(PostsCreateSchema, location='json')
    @posts.response(200, PostSchema(only=(
            'id', 'title', 'text', 'views', 'user', 'created_at'
    )))
    def post(self, data):
        post = Post(user_id=g.user.id, **data)
        post.save()

        return post


@posts.route('/<post_id>')
class PostsById(MethodView):
    @posts.response(200, PostSchema(only=(
            'id', 'title', 'text', 'views', 'user', 'created_at'
    )))
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        if post.deleted:
            return abort(404)
        
        post.views = post.views + 1
        post.save()

        return post

    @auth_required
    @developer_required
    @posts.arguments(PostsUpdateSchema, location='json')
    @posts.response(200, PostSchema(only=(
            'id', 'title', 'text', 'views', 'user', 'created_at'
    )))
    def put(self, data, post_id):
        post = Post.query.get_or_404(post_id)

        if post.deleted:
            return abort(404)

        for key, value in data.items():
            setattr(post, key, value)

        post.save()

        return post

    @auth_required
    @developer_required
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        if post.deleted:
            return abort(404)

        post.deleted = True
        post.save()

        return jsonify({
            'message': 'success deleting'
        }), 200
