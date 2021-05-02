from flask import abort, jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc, asc
from middlewares import auth_required, developer_required
from schemas.filters import FiltersQueryArgsSchema
from schemas.worker import WorkersListSchema, WorkerSchema, WorkersCreateSchema, WorkersUpdateSchema
from models.worker import Worker

workers = Blueprint('workers', 'workers', url_prefix='/workers')


@workers.route('/')
class Vehicles(MethodView):
    @workers.arguments(FiltersQueryArgsSchema, location='query')
    @workers.response(200, WorkersListSchema)
    def get(self, arguments):
        order_column = arguments['order']['column']
        order_type = arguments['order']['type']

        arguments['filters']['deleted'] = False

        query = Worker.query.filter_by(**arguments['filters'])
        count = query.count()

        query = query.order_by(
            desc(order_column) if order_type == 'desc' else asc(order_column)
        )
        if arguments['per_page']['limit'] != 0:
            query = query.limit(arguments['per_page']['limit'])
            query = query.offset(arguments['per_page']['offset'])

        return {
            'workers': query.all(),
            'count': count
        }

    @auth_required
    @developer_required
    @workers.arguments(WorkersCreateSchema, location='json')
    @workers.response(200, WorkerSchema(only=(
            'first_name', 'last_name', 'patronymic', 'show_full_name', 'used', 'id'
    )))
    def post(self, data):
        worker = Worker(user_id=g.user.id, **data)
        worker.save()

        return worker


@workers.route('/<worker_id>')
class VehiclesById(MethodView):
    @workers.response(200, WorkerSchema(only=(
            'first_name', 'last_name', 'patronymic', 'show_full_name', 'used', 'id'
    )))
    def get(self, worker_id):
        worker = Worker.query.get_or_404(worker_id)
        if worker.deleted:
            return abort(404)

        return worker

    @auth_required
    @developer_required
    @workers.arguments(WorkersUpdateSchema, location='json')
    @workers.response(200, WorkerSchema(only=(
            'first_name', 'last_name', 'patronymic', 'show_full_name', 'used', 'id'
    )))
    def put(self, data, worker_id):
        worker = Worker.query.get_or_404(worker_id)

        if worker.deleted:
            return abort(404)

        for key, value in data.items():
            setattr(worker, key, value)
        if 'patronymic' in data:
            if data['patronymic'] == '':
                worker.patronymic = None
        worker.save()

        return worker

    @auth_required
    @developer_required
    def delete(self, worker_id):
        worker = Worker.query.get_or_404(worker_id)
        if worker.deleted:
            return abort(404)

        worker.deleted = True
        worker.save()

        return jsonify({
            'message': 'success deleting'
        }), 200
