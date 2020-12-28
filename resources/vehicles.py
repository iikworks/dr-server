from flask import abort, jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc, asc
from middlewares import auth_required, developer_required
from schemas.filters import FiltersQueryArgsSchema
from schemas.vehicle import VehiclesListSchema, VehicleSchema, VehiclesCreateSchema, VehiclesUpdateSchema
from models.vehicle import Vehicle

vehicles = Blueprint('vehicles', 'vehicles', url_prefix='/vehicles')


@vehicles.route('/')
class Vehicles(MethodView):
    @vehicles.arguments(FiltersQueryArgsSchema, location='query')
    @vehicles.response(VehiclesListSchema, code=200)
    def get(self, arguments):
        order_column = arguments['order']['column']
        order_type = arguments['order']['type']

        arguments['filters']['deleted'] = False

        query = Vehicle.query.filter_by(**arguments['filters'])
        count = query.count()

        query = query.order_by(
            desc(order_column) if order_type == 'desc' else asc(order_column)
        )
        if arguments['per_page']['limit'] != 0:
            query = query.limit(arguments['per_page']['limit'])
            query = query.offset(arguments['per_page']['offset'])

        return {
            'vehicles': query.all(),
            'count': count
        }

    @auth_required
    @developer_required
    @vehicles.arguments(VehiclesCreateSchema, location='json')
    @vehicles.response(VehicleSchema(only=(
        'type',
        'brand',
        'model',
        'government_number',
        'government_number_letters',
        'government_number_region',
        'year_of_ussue',
        'user',
        'worker',
        'used',
        'id',
        'type_display'
    )), code=200)
    def post(self, data):
        data['v_type'] = data['type']
        del data['type']

        vehicle = Vehicle(user_id=g.user.id, **data)
        vehicle.save()

        return vehicle


@vehicles.route('/<vehicle_id>')
class VehiclesById(MethodView):
    @vehicles.response(VehicleSchema(only=(
        'type',
        'brand',
        'model',
        'government_number',
        'government_number_letters',
        'government_number_region',
        'year_of_ussue',
        'user',
        'worker',
        'used',
        'id',
        'type_display'
    )), code=200)
    def get(self, vehicle_id):
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        if vehicle.deleted:
            return abort(404)

        return vehicle

    @auth_required
    @developer_required
    @vehicles.arguments(VehiclesUpdateSchema, location='json')
    @vehicles.response(VehicleSchema(only=(
        'type',
        'brand',
        'model',
        'government_number',
        'government_number_letters',
        'government_number_region',
        'year_of_ussue',
        'user',
        'worker',
        'used',
        'id',
        'type_display'
    )), code=200)
    def put(self, data, vehicle_id):
        vehicle = Vehicle.query.get_or_404(vehicle_id)

        if vehicle.deleted:
            return abort(404)

        for key, value in data.items():
            setattr(vehicle, key, value)
        if 'government_number' in data:
            if data['government_number'] == 0:
                vehicle.government_number = None
        vehicle.save()

        return vehicle

    @auth_required
    @developer_required
    def delete(self, vehicle_id):
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        if vehicle.deleted:
            return abort(404)

        vehicle.deleted = True
        vehicle.save()

        return jsonify({
            'message': 'success deleting'
        }), 200
