import io
import logging
from flask import Flask, Response
from flask_restful import Resource, Api
from resources.rest.sqlalchemy.email import *
from resources.rest.sqlalchemy.upload import *
from resources.rest.sqlalchemy.dataSourceConfig import *
from resources.rest.sqlalchemy.safxtable import *
from resources.rest.sqlalchemy.dstable import *
from resources.rest.sqlalchemy.schedules import *
#from resources.rest.sqlalchemy.schedulelog import *

logging.basicConfig(filename='api_taxone_flask_restfull.log', level=logging.DEBUG)


class OURFlask(Flask):
    logger = logging.getLogger(__name__ + '.OURFlask')
    def make_default_options_response(self):
        self.logger.debug('in cors make_default_options_response')
        response = Response(
            response='',
            status=200,
        )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,POST,PUT,DELETE,TRACE,OPTIONS,PATCH'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = '1800'
        response.headers['Access-Control-Allow-Headers'] = 'authorization, Content-Type'
        response.headers['Allow'] = 'GET, HEAD, POST, PUT, DELETE, TRACE, OPTIONS, PATCH'
        return response
        
app = OURFlask(__name__)
api = Api(app)

api.add_resource(EmailController, '/emails')
api.add_resource(EmailByIdController, '/emails/<id>')
api.add_resource(UploadController, '/uploads')
api.add_resource(DataSourceConfigsController, '/dataSourceConfigs')
api.add_resource(DataSourceConfigsDSTableController, '/dataSourceConfigs/<dataSourceType>/dsTables')
api.add_resource(DataSourceConfigsDSColumnsController, '/dataSourceConfigs/<dataSourceType>/dsTables/<dsTableId>/dsColumns')
api.add_resource(DataSourceConfigsMetadataController, '/dataSourceConfigs/<dataSourceType>/metadata')
api.add_resource(DataSourceConfigsObjectController, '/dataSourceConfigs/<dataSourceType>')
api.add_resource(SAFXTableListController, '/safxTables')
api.add_resource(SAFXTableColumnsController, '/safxTables/<id>/safxColumns')
api.add_resource(SAFXTableObjectController, '/safxTables/<id>')
api.add_resource(SAFXTableDSTableController, '/safxTables/<id>/dsTables/<dsTableId>')
api.add_resource(DSTableController, '/dsTables')
api.add_resource(DSColumnController, '/dsTables/<id>/dsColumns')
api.add_resource(ScheduleListController, '/schedules')
api.add_resource(ScheduleObjectController, '/schedules', '/schedules/<id>')
api.add_resource(SchedulePeriodsController, '/schedules/<id>/periodes')


if __name__ == '__main__':
    app.run()