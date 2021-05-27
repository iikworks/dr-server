from flask import abort, jsonify, g
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc, asc
from middlewares import auth_required, developer_required
from schemas.filters import FiltersQueryArgsSchema
from schemas.cardnumbers import CardNumbersListSchema, CardNumberSchema, CardNumbersCreateSchema, CardNumbersUpdateSchema
from models.cardnumber import CardNumber

cardnumbers = Blueprint('cardnumbers', 'cardnumbers', url_prefix='/cardnumbers')


@cardnumbers.route('/')
class CardNumbers(MethodView):
    @cardnumbers.response(200, CardNumbersListSchema)
    def get(self):
        query = CardNumber.query.filter_by(deleted=False)

        query = query.order_by(
            desc('id')
        )

        return {
            'cardnumbers': query.all(),
        }

    @auth_required
    @developer_required
    @cardnumbers.arguments(CardNumbersCreateSchema, location='json')
    @cardnumbers.response(200, CardNumberSchema(only=(
        'title', 'number', 'user', 'created_at', 'id'
    )))
    def post(self, data):
        cardnumber = CardNumber(user_id=g.user.id, **data)
        cardnumber.save()

        return cardnumber


@cardnumbers.route('/<cardnumber_id>')
class CardNumbersById(MethodView):
    @auth_required
    @developer_required
    @cardnumbers.arguments(CardNumbersUpdateSchema, location='json')
    @cardnumbers.response(200, CardNumberSchema(only=(
        'title', 'number', 'user', 'created_at', 'id'
    )))
    def put(self, data, cardnumber_id):
        cardnumber = CardNumber.query.get_or_404(cardnumber_id)

        if cardnumber.deleted:
            return abort(404)

        for key, value in data.items():
            setattr(cardnumber, key, value)
        
        cardnumber.save()

        return cardnumber

    @auth_required
    @developer_required
    def delete(self, cardnumber_id):
        cardnumber = CardNumber.query.get_or_404(cardnumber_id)
        if cardnumber.deleted:
            return abort(404)

        cardnumber.deleted = True
        cardnumber.save()

        return jsonify({
            'message': 'success deleting'
        }), 200
