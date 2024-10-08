import sys
import io
import logging
import json
from flask import Response, request, jsonify
from flask_restful import Resource, Api
from werkzeug.datastructures import * #.Headers

from entity import *
from util.util import *

class SAFXTableListController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableListController')
    
    def get(self):
        self.logger.debug('in list_safxtables')
        try: 
            page = int(request.args.get('page'))
            size = int(request.args.get('size'))
            safxtables = SAFXTable.select().paginate(page+1, size)
            safxtablesJson = '{"content": [], "totalPages": 0}'
            if (len(safxtables) > 0):
                count = len(SAFXTable.select())
                totalPages = int(count / size) + 1 if count % size != 0 else 0
                safxtablesJson = wrap(safxtables, totalPages)
            self.logger.debug('safxtablesJson:' + safxtablesJson)
            return generate_http200ok(safxtablesJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


class SAFXTableColumnsController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableColumnsController')
    
    def get(self, id):
        self.logger.debug('in list_safxcoluimns')
        try: 
            safxcolumns = SAFXColumn.select().join(SAFXTable).where(SAFXTable.id==id)
            safxcolumnsJson = '[]'
            if (len(safxcolumns) > 0):
                safxcolumnsJson = wraplist(safxcolumns)
            self.logger.debug('safxcolumnsJson:' + safxcolumnsJson)
            return generate_http200ok(safxcolumnsJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []

    def put(self, id):
        self.logger.debug('in update_safxcolumn - id' + str(id))
        safxcolumnsListRaw = request.data
        safxcolumnsListBytes = io.BytesIO(safxcolumnsListRaw)
        safxcolumnsList = json.load(safxcolumnsListBytes)
        self.logger.debug('safxcolumnsListBytes:' + str(safxcolumnsListBytes.getvalue(), encoding='utf-8'))
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
        return generate_http200ok()                


class SAFXTableObjectController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableObjectController')
    
    def get(self, id):
        self.logger.debug('in get_safxtable:' + str(id))
        try: 
            safxtable = SAFXTable.get(id)
            safxtablesJson = safxtable.toJson()
            self.logger.debug('safxtablesJson:' + safxtablesJson)
            return generate_http200ok(safxtablesJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


    def put(self):
        self.logger.debug('in update_safxtable')
        safxtablesListRaw = request.data
        self.logger.debug('safxtablesListRaw:' + safxtablesListRaw)
        safxtablesListBytes = io.BytesIO(safxtablesListRaw)
        safxtablesList = json.load(safxtablesListBytes)
        safxtablesEntity = []
        for safxtable in safxtablesList:
            if safxtable.get('id'):
                SAFXTable.update(**safxtable)
            else:
                SAFXTable.create(**safxtable)
        return generate_http200ok()

class SAFXTableDSTableController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableDSTableController')
    
    def put(self, id, dsTableId):
        self.logger.debug('in update_safxtable_dstable')
        dsTable = DSTable.select().where(DSTable.id==dsTableId)
        safxTable = SAFXTable.update(dsTable=dsTable).where(SAFXTable.id == id)
        self.logger.debug('safxTable.sql():')
        self.logger.debug(safxTable.sql())
        safxTable.execute()
        return generate_http200ok()

