import http.client
from datetime import datetime
from flask_restplus import Namespace, Resource, fields
from areas_backend import config
from areas_backend.models import AreaModel
from areas_backend.token_validation import validate_token_header
from areas_backend.db import db
from flask import abort

api_namespace = Namespace('api', description='API operations')


def authentication_header_parser(value):
    username = validate_token_header(value, config.PUBLIC_KEY)
    if username is None:
        abort(401)
    return username


# Input and output formats for area

authentication_parser = api_namespace.parser()
authentication_parser.add_argument('Authorization', location='headers',
                                   type=str,
                                   help='Bearer Access Token')

area_parser = authentication_parser.copy()
area_parser.add_argument('areacode', type=str, required=True,
                         help='3 characters of the area')
area_parser.add_argument('area', type=str, required=True,
                         help='Text of the area')
area_parser.add_argument('zonecode', type=str, required=True,
                         help='3 characters of the State')

model = {
    'id': fields.Integer(),
    'username': fields.String(),
    'areacode': fields.String(),
    'area': fields.String(),
    'zonecode': fields.String(),
    'timestamp': fields.DateTime(),
}
area_model = api_namespace.model('Area', model)


@api_namespace.route('/me/areas/')
class MeAreaListCreate(Resource):

    @api_namespace.doc('list_areas')
    @api_namespace.expect(authentication_parser)
    @api_namespace.marshal_with(area_model, as_list=True)
    def get(self):
        '''
        Retrieves all the areas
        '''
        args = authentication_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        areas = (AreaModel
                 .query
                 .filter(AreaModel.username == username)
                 .order_by('id')
                 .all())
        return areas

    @api_namespace.doc('create_area')
    @api_namespace.expect(area_parser)
    @api_namespace.marshal_with(area_model, code=http.client.CREATED)
    def post(self):
        '''
        Create a new area
        '''
        args = area_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        new_area = AreaModel(username=username,
                             areacode=args['areacode'],
                             area=args['area'],
                             zonecode=args['zonecode'],
                             timestamp=datetime.utcnow())
        db.session.add(new_area)
        db.session.commit()

        result = api_namespace.marshal(new_area, area_model)

        return result, http.client.CREATED


search_parser = api_namespace.parser()
search_parser.add_argument('search', type=str, required=False,
                           help='Search in the text of the areas')


@api_namespace.route('/areas/')
class AreaList(Resource):

    @api_namespace.doc('list_areas')
    @api_namespace.marshal_with(area_model, as_list=True)
    @api_namespace.expect(search_parser)
    def get(self):
        '''
        Retrieves all the areas
        '''
        args = search_parser.parse_args()
        search_param = args['search']
        query = AreaModel.query
        if search_param:
            param = f'%{search_param}%'
            query = (query.filter(AreaModel.area.ilike(param)))
            # Old code, that it's not case insensitive in postgreSQL
            # query = (query.filter(AreaModel.text.contains(search_param)))

        query = query.order_by('id')
        areas = query.all()

        return areas


@api_namespace.route('/areas/<int:area_id>/')
class AreasRetrieve(Resource):

    @api_namespace.doc('retrieve_area')
    @api_namespace.marshal_with(area_model)
    def get(self, area_id):
        '''
        Retrieve a area
        '''
        area = AreaModel.query.get(area_id)
        if not area:
            # The area is not present
            return '', http.client.NOT_FOUND

        return area
