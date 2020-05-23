import http.client
from flask_restplus import Namespace, Resource
from areas_backend.models import AreaModel
from areas_backend.db import db

admin_namespace = Namespace('admin', description='Admin operations')


@admin_namespace.route('/areas/<int:area_id>/')
class AreasDelete(Resource):

    @admin_namespace.doc('delete_area',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, area_id):
        '''
        Delete a area
        '''
        area = AreaModel.query.get(area_id)
        if not area:
            # The area is not present
            return '', http.client.NO_CONTENT

        db.session.delete(area)
        db.session.commit()

        return '', http.client.NO_CONTENT
