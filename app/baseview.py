from flask_restful import Resource, Api, reqparse, marshal, inputs, request
from sqlalchemy import desc
from . import db, app
from .util import admin_required

api = Api(app)

class BaseView(Resource):

    def __init__(self, model=None):
        self.model = model

    def response(self, data={}, rescode='0000', title='SUCCESS', body='SUCCESS', code=200, headers=None):
        data = {
            'rescode': rescode,
            'message': {
                'title': title,
                'body': body
            }
            # 'data': res_data
        }

        res = api.make_response(data, code)
        res.headers.extend(headers or {})
        return res


class BaseCrud(BaseView, Resource):

    @admin_required
    def get(self, id=None):
        if id is not None:
            qry = self.model.query.get(id)
            if qry is not None:
                return marshal(qry, self.model.response_fields), 200, {'Content-Type': 'application/json'}
            return {'status': 'User Not Found'}, 404, {'Content-Type': 'application/json'}
        else:
            return {'status': 'id Please'}, 400, {'Content-Type': 'application/json'}

    @admin_required
    def post(self):
        pass

    @admin_required
    def put(self, id=None):
        pass

    @admin_required
    def delete(self, id):
        qry = self.model.query.get(id)
        if qry is None:
            return {'status': 'User Not Found'}, 404, {'Content-Type': 'application/json'}

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'User Deleted'}, 200, {'Content-Type': 'application/json'}

class BaseViewList(BaseView):

    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', choices=('id'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = self.model.query

        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(self.model.id))
                else:
                    qry = qry.order_by((self.model.id))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, self.model.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}

