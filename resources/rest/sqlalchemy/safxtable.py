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

class SAFXTableListController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableListController')
    
    def get(self):
        self.logger.debug('in list_safxtables')
        session = Session(engine)
        try: 
            page = int(request.args.get('page'))
            size = int(request.args.get('size'))
            safxtablesStt = select(SAFXTable).limit(size).offset((page)*size)
            safxtables = session.scalars(safxtablesStt).fetchall()
            safxtablesJson = '{"content": [], "totalPages": 0}'
            if (len(safxtables) > 0):
                safxtablesAllStt = select(SAFXTable).limit(size).offset((page)*size)
                safxtablesAll = session.scalars(safxtablesAllStt).fetchall()
                count = len(safxtablesAll)
                totalPages = int(count / size) + 1 if count % size != 0 else 0
                safxtablesJson = wrap(safxtables, totalPages)
            self.logger.debug('safxtablesJson:' + safxtablesJson)
            http200okresponse.set_data(safxtablesJson)
            return http200okresponse
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


class SAFXTableColumnsController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableColumnsController')
    
    def get(self, id):
        self.logger.debug('in list_safxcoluimns')
        session = Session(engine)
        try: 
            safxcolumnsStt = select(SAFXColumn).join(SAFXTable).where(SAFXTable.id==int(id))
            safxcolumns = session.scalars(safxcolumnsStt).fetchall()
            safxcolumnsJson = '[]'
            if (len(safxcolumns) > 0):
                safxcolumnsJson = wraplist(safxcolumns)
            self.logger.debug('safxcolumnsJson:' + safxcolumnsJson)
            http200okresponse.set_data(safxcolumnsJson)
            return http200okresponse
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []

    def put(self, id):
        self.logger.debug('in update_safxcolumn - id' + str(id))
        session = Session(engine)
        safxcolumnsListRaw = request.data
        safxcolumnsListBytes = io.BytesIO(safxcolumnsListRaw)
        safxcolumnsList = json.load(safxcolumnsListBytes)
        self.logger.debug('safxcolumnsListBytes:' + str(safxcolumnsListBytes.getvalue(), encoding='utf-8'))
        safxcolumnsEntity = []
        for safxcolumn in safxcolumnsList:
            dsColumnId = safxcolumn.get('dsColumnId')
            dsColumn = None
            if dsColumnId:
                dsColumnsStt = select(DSColumn).where(DSColumn.id==dsColumnId)
                dsColumns = session.scalars(dsColumnsStt).fetchall()
                dsColumn = dsColumns[0]
            safxColumnEntitysStt = select(SAFXColumn).where(SAFXColumn.id==safxcolumn['id'])
            safxColumnEntitys = session.scalars(safxColumnEntitysStt).fetchall()
            safxColumnEntity = safxColumnEntitys[0]
            safxColumnEntity.dsColumn=dsColumn
            session.add(safxColumnEntity)
            session.commit()
                
        return http200okresponse

class SAFXTableObjectController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableObjectController')
    
    def get(self, id):
        self.logger.debug('in get_safxtable:' + str(id))
        session = Session(engine)
        try: 
            safxtablesStt = select(SAFXTable).where(SAFXTable.id==int(id))
            safxtables = session.scalars(safxtablesStt).fetchall()
            safxtable = safxtables[0]
            #safxtable = SAFXTable.get(id)
            safxtablesJson = safxtable.toJson()
            self.logger.debug('safxtablesJson:' + safxtablesJson)
            http200okresponse.set_data(safxtablesJson)
            return http200okresponse
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


    def put(self):
        self.logger.debug('in update_safxtable')
        session = Session(engine)
        safxtablesListRaw = request.data
        self.logger.debug('safxtablesListRaw:' + safxtablesListRaw)
        safxtablesListBytes = io.BytesIO(safxtablesListRaw)
        safxtablesList = json.load(safxtablesListBytes)
        safxtablesEntity = []
        for safxtable in safxtablesList:
            if safxtable.get('id'):
                #SAFXTable.update(**safxtable)
                pass
            else:
                #SAFXTable.create(**safxtable)
                pass
        return http200okresponse


class SAFXTableDSTableController(Resource):
    logger = logging.getLogger(__name__ + '.SAFXTableDSTableController')
    
    def put(self, id, dsTableId):
        self.logger.debug('in update_safxtable_dstable')
        session = Session(engine)
        dsTablesStt = select(DSTable).where(DSTable.id==dsTableId)
        dsTables = session.scalars(dsTablesStt).fetchall()
        dsTable = dsTables[0]
        safxTablesStt = select(SAFXTable).where(SAFXTable.id == id)
        safxTables = session.scalars(safxTablesStt).fetchall()
        safxTable = safxTables[0]
        self.logger.debug('safxTable.sql():')
        session.add(safxTable)
        session.commit()
        return http200okresponse

