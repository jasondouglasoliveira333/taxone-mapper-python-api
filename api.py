import io
from flask import Flask, Response
from resources.email import *
from resources.upload import *
from resources.dataSourceConfig import *
from resources.safxtable import *
from resources.dstable import *


class OURFlask(Flask):
    def make_default_options_response(self):
        print('in cors make_default_options_response')
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

app.add_url_rule('/emails', view_func=list_emails, methods= ['GET'])
app.add_url_rule('/emails', view_func=insert_update_email, methods= ['POST'])
app.add_url_rule('/emails/<id>', view_func=delete_email, methods= ['DELETE'])
app.add_url_rule('/uploads', view_func=list_uploads, methods= ['GET'])
app.add_url_rule('/uploads', view_func=insert_upload, methods= ['POST'])
app.add_url_rule('/dataSourceConfigs', view_func=list_data_source_configs, methods= ['GET'])
app.add_url_rule('/dataSourceConfigs/<dataSourceType>/dsTables', view_func=list_dsTables, methods= ['GET'])
app.add_url_rule('/dataSourceConfigs/<dataSourceType>/dsTables/<dsTableId>/dsColumns', view_func=list_dsColumns, methods= ['GET'])
app.add_url_rule('/dataSourceConfigs/<dataSourceType>/metadata', view_func=get_metadata, methods= ['POST'])
app.add_url_rule('/dataSourceConfigs/<dataSourceType>', view_func=insert_dsConfiguration, methods= ['POST'])
app.add_url_rule('/dataSourceConfigs/<dataSourceType>', view_func=get_data_source_config, methods= ['GET'])
app.add_url_rule('/safxTables', view_func=list_safxtables, methods= ['GET'])
app.add_url_rule('/safxTables/<id>/safxColumns', view_func=list_safxcoluimns, methods= ['GET'])
app.add_url_rule('/safxTables/<id>', view_func=get_safxtable, methods= ['GET'])
app.add_url_rule('/safxTables/<id>', view_func=update_safxtable, methods= ['PUT'])
app.add_url_rule('/safxTables/<id>/safxColumns', view_func=update_safxcolumn, methods= ['PUT'])
app.add_url_rule('/dsTables', view_func=list_dstables, methods= ['GET'])
app.add_url_rule('/dsTables/<id>/dsColumns', view_func=list_dsTable_dsColumns, methods= ['GET'])
app.add_url_rule('/safxTables/<id>/dsTables/<dsTableId>', view_func=update_safxtable_dstable, methods= ['PUT'])


if __name__ == '__main__':
    app.run()