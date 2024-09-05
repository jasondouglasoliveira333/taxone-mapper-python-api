import sys
import io
import logging
import json
from flask import Response, request, jsonify
from flask_restful import Resource, Api
from werkzeug.datastructures import * #.Headers

from entity import *
from util import *

class DSTableController(Resource):
    logger = logging.getLogger(__name__ + '.DSTableController')
    def get(self):
        self.logger.info('in list_dstables')
        try: 
            dstables = DSTable.select()
            dstablesJson = '[]'
            if (len(dstables) > 0):
                dstablesJson = wraplist(dstables)
            self.logger.info('dstablesJson:' + dstablesJson)
            http200okresponse.set_data(dstablesJson)
            return http200okresponse
        except:    
            self.logger.info('sys.exception():' + repr(sys.exception()))
            return []

class DSColumnController(Resource):
    logger = logging.getLogger(__name__ + '.DSColumnController')
    def get(self, id):
        self.logger.info('in list_dsTable_dsColumns')
        try: 
            dscolumns = DSColumn.select().join(DSTable).where(DSTable.id==id)
            #self.logger.info('dscolumns.sql()', dscolumns.sql())
            dscolumnsJson = '{"content": [], "totalPages": 0}'
            if (len(dscolumns) > 0):
                dscolumnsJson = wrap(dscolumns)
            self.logger.info('dscolumnsJson:' + dscolumnsJson)
            http200okresponse.set_data(dscolumnsJson)
            return http200okresponse
        except:    
            self.logger.info('sys.exception():' + repr(sys.exception()))
            return []
        