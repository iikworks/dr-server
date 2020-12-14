from flask import abort, jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from middlewares import auth_required, developer_required
from schemas.homestats import HomeStatsSchema, HomeStatsCreateSchema, HomeStatsUpdateSchema, HomeStatsListSchema
from models.homestats import HomeStats

homestats = Blueprint('homestats', 'homestats', url_prefix='/homestats')


@homestats.route('/')
class HomeStatsList(MethodView):
    @homestats.response(HomeStatsListSchema, code=200)
    def get(self):
        homestats_list = HomeStats.query.filter_by(deleted=False).all()

        return {
            'homestats': homestats_list
        }

    @auth_required
    @developer_required
    @homestats.arguments(HomeStatsCreateSchema, location='json')
    @homestats.response(HomeStatsSchema(only=(
        'type',
        'title',
        'place',
        'position',
        'liquid',
        'id',
        'user',
        'created_at'
    )), code=200)
    def post(self, data):
        data['stat_type'] = data['type']
        del data['type']

        homestat = HomeStats(user_id=g.user.id, **data)
        homestat.save()

        return homestat


@homestats.route('/<homestat_id>')
class HomeStatsById(MethodView):
    @homestats.response(HomeStatsSchema(only=(
        'type',
        'title',
        'place',
        'position',
        'liquid',
        'id',
        'user',
        'created_at'
    )), code=200)
    def get(self, homestat_id):
        homestat = HomeStats.query.get_or_404(homestat_id)
        if homestat.deleted:
            return abort(404)

        return homestat

    @auth_required
    @developer_required
    @homestats.arguments(HomeStatsUpdateSchema, location='json')
    @homestats.response(HomeStatsSchema(only=(
        'type',
        'title',
        'place',
        'position',
        'liquid',
        'id',
        'user',
        'created_at'
    )), code=200)
    def put(self, data, homestat_id):
        homestat = HomeStats.query.get_or_404(homestat_id)

        if homestat.deleted:
            return abort(404)

        for key, value in data.items():
            setattr(homestat, key, value)

        homestat.save()

        return homestat

    @auth_required
    @developer_required
    def delete(self, homestat_id):
        homestat = HomeStats.query.get_or_404(homestat_id)
        if homestat.deleted:
            return abort(404)

        homestat.deleted = True
        homestat.save()

        return jsonify({
            'message': 'success deleting'
        }), 200
