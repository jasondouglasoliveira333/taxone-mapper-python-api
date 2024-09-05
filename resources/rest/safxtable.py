import sys
import io
import logging
import json
from flask import Response, request, jsonify
from flask_restful import Resource, Api
from werkzeug.datastructures import * #.Headers

from entity import *
from util import *

class SAFXTableListController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableListController')
    def get(self):
        self.logger.info('in list_safxtables')
        try: 
            page = request.args.get('page')
            size = request.args.get('size')
            safxtables = SAFXTable.select()
            safxtablesJson = '{"content": [], "totalPages": 0}'
            if (len(safxtables) > 0):
                safxtablesJson = wrap(safxtables)
            self.logger.info('safxtablesJson:' + safxtablesJson)
            http200okresponse.set_data(safxtablesJson)
            return http200okresponse
        except:    
            self.logger.info('sys.exception():' + repr(sys.exception()))
            return []


class SAFXTableColumnsController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableColumnsController')
    def get(self, id):
        self.logger.info('in list_safxcoluimns')
        try: 
            page = request.args.get('page')
            size = request.args.get('size')
            safxcolumns = SAFXColumn.select().join(SAFXTable).where(SAFXTable.id==id)
            safxcolumnsJson = '[]'
            if (len(safxcolumns) > 0):
                safxcolumnsJson = wraplist(safxcolumns)
            self.logger.info('safxcolumnsJson:' + safxcolumnsJson)
            http200okresponse.set_data(safxcolumnsJson)
            return http200okresponse
        except:    
            self.logger.info('sys.exception():' + repr(sys.exception()))
            return []

    def put(self, id):
        self.logger.info('in update_safxcolumn - id' + str(id))
        safxcolumnsListRaw = request.data
        safxcolumnsListBytes = io.BytesIO(safxcolumnsListRaw)
        safxcolumnsList = json.load(safxcolumnsListBytes)
        self.logger.info('safxcolumnsListBytes:' + str(safxcolumnsListBytes.getvalue(), encoding='utf-8'))
        safxcolumnsEntity = []
        for safxcolumn in safxcolumnsList:
            dsColumnId = safxcolumn.get('dsColumnId')
            dsColumn = None
            if dsColumnId:
                dsColumns = DSColumn.select().where(DSColumn.id==dsColumnId)
                dsColumn = dsColumns[0]
            safxColumnEntitys = SAFXColumn.select().where(SAFXColumn.id==safxcolumn['id'])
            safxColumnEntity = safxColumnEntitys[0]
            safxColumnEntity.dsColumn=dsColumn
            safxColumnEntity.save()
                
        return http200okresponse

class SAFXTableObjectController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableObjectController')
    def get(self, id):
        self.logger.info('in get_safxtable:' + str(id))
        try: 
            safxtable = SAFXTable.get(id)
            safxtablesJson = safxtable.toJson()
            self.logger.info('safxtablesJson:' + safxtablesJson)
            http200okresponse.set_data(safxtablesJson)
            return http200okresponse
        except:    
            self.logger.info('sys.exception():' + repr(sys.exception()))
            return []


    def put(self):
        self.logger.info('in update_safxtable')
        safxtablesListRaw = request.data
        self.logger.info('safxtablesListRaw:' + safxtablesListRaw)
        safxtablesListBytes = io.BytesIO(safxtablesListRaw)
        safxtablesList = json.load(safxtablesListBytes)
        safxtablesEntity = []
        for safxtable in safxtablesList:
            if safxtable.get('id'):
                SAFXTable.update(**safxtable)
            else:
                SAFXTable.create(**safxtable)
        return http200okresponse


class SAFXTableDSTableController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableDSTableController')
    def put(self, id, dsTableId):
        self.logger.info('in update_safxtable_dstable')
        dsTable = DSTable.select().where(DSTable.id==dsTableId)
        safxTable = SAFXTable.update(dsTable=dsTable).where(SAFXTable.id == id)
        self.logger.info('safxTable.sql():')
        self.logger.info(safxTable.sql())
        safxTable.execute()
        return http200okresponse

