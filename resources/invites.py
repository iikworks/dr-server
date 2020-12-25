import datetime

from flask.views import MethodView
from flask_smorest import Blueprint
from middlewares import auth_required, developer_required
from schemas.invite import InvitesListSchema, InviteUpdateSchema, InviteSchema
from models.invite import Invite

invites = Blueprint('invites', 'invites', url_prefix='/invites')


@invites.route('/')
class Vehicles(MethodView):
    @invites.response(InvitesListSchema, code=200)
    def get(self):
        query = Invite.query

        return {
            'invites': query.all(),
        }

    @auth_required
    @developer_required
    @invites.response(InviteSchema(only=(
            'code', 'used', 'used_at', 'user', 'created_at', 'id'
    )), code=200)
    def post(self):
        invite = Invite()
        invite.save()

        return invite


@invites.route('/<invite_id>')
class VehiclesById(MethodView):
    @invites.response(InviteSchema(only=(
            'code', 'used', 'used_at', 'user', 'created_at', 'id'
    )), code=200)
    def get(self, invite_id):
        invite = Invite.query.get_or_404(invite_id)

        return invite

    @auth_required
    @developer_required
    @invites.arguments(InviteUpdateSchema, location='json')
    @invites.response(InviteSchema(only=(
            'code', 'used', 'used_at', 'user', 'created_at', 'id'
    )), code=200)
    def put(self, data, invite_id):
        invite = Invite.query.get_or_404(invite_id)

        if 'used' in data:
            invite.used = data['used']
            if invite.used:
                invite.used_at = datetime.datetime.now()
            else:
                invite.used_at = None

        return invite