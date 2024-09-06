import sys
import io
import logging
import json

from flask import Response, request, jsonify
from flask_restful import Resource, Api

from sqlalchemy.orm import Session
from sqlalchemy import select

from entity import *
from util import *

class DSTableController(Resource):
    logger = logging.getLogger(__name__ + '.DSTableController')
    
    def get(self):
        self.logger.debug('in list_dstables')
        try: 
            session = Session(engine)
            dstablesStt = select(DSTable)
            dstables = session.scalars(dstablesStt).fetchall()
            #dstables = DSTable.select()
            dstablesJson = '[]'
            if (len(dstables) > 0):
                dstablesJson = wraplist(dstables)
            self.logger.debug('dstablesJson:' + dstablesJson)
            http200okresponse.set_data(dstablesJson)
            return http200okresponse
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []

class DSColumnController(Resource):
    logger = logging.getLogger(__name__ + '.DSColumnController')
    
    def get(self, id):
        self.logger.debug('in list_dsTable_dsColumns')
        try: 
            session = Session(engine)
            dsColumnsStt = select(DSColumn).join(DSTable).where(DSTable.id==id)
            dsColumns = session.scalars(dsColumnsStt).fetchall()
            dscolumnsJson = '{"content": [], "totalPages": 0}'
            if (len(dsColumns) > 0):
                dscolumnsJson = wrap(dsColumns)
            self.logger.debug('dscolumnsJson:' + dscolumnsJson)
            http200okresponse.set_data(dscolumnsJson)
            return http200okresponse
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []
        