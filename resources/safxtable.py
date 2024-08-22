import sys
import io
import json
from flask import Response, request, jsonify
from werkzeug.datastructures import * #.Headers

from entity import *
from util import *

def list_safxtables():
    print('in list_safxtables')
    try: 
        page = request.args.get('page')
        size = request.args.get('size')
        safxtables = SAFXTable.select()
        #print('safxtables.sql()', safxtables.sql())
        safxtablesJson = '{"content": [], "totalPages": 0}'
        if (len(safxtables) > 0):
            safxtablesJson = wrap(safxtables)
        print('safxtablesJson:', safxtablesJson)
        http200okresponse.set_data(safxtablesJson)
        return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


def update_safxtable():
    print('in update_safxtable')
    safxtablesListRaw = request.data
    print('safxtablesListRaw:', safxtablesListRaw)
    safxtablesListBytes = io.BytesIO(safxtablesListRaw)
    safxtablesList = json.load(safxtablesListBytes)
    safxtablesEntity = []
    for safxtable in safxtablesList:
        if safxtable.get('id'):
            SAFXTable.update(**safxtable)
        else:
            SAFXTable.create(**safxtable)
    return http200okresponse


def list_safxcoluimns(id):
    print('in list_safxcoluimns')
    try: 
        page = request.args.get('page')
        size = request.args.get('size')
        safxcolumns = SAFXColumn.select().join(SAFXTable).where(SAFXTable.id==id)
        #print('safxcolumns.sql()', safxcolumns.sql())
        safxcolumnsJson = '[]'
        if (len(safxcolumns) > 0):
            safxcolumnsJson = wraplist(safxcolumns)
        print('safxcolumnsJson:', safxcolumnsJson)
        OURheader = Headers()
        OURheader.add('access-control-allow-origin', '*')
        http200okresponse.set_data(safxcolumnsJson)
        print('http200okresponse.__hash__  - list_safxcoluimns:' + str(http200okresponse.__hash__))
        return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


def get_safxtable(id):
    print('in get_safxtable:', id)
    try: 
        safxtable = SAFXTable.get(id)
        safxtablesJson = safxtable.toJson()
        #safxtablesJson = '{"content": [], "totalPages": 0}'
        #if (len(safxtables) > 0):
        #    safxtablesJson = wrap(safxtables)
        print('safxtablesJson:', safxtablesJson)
        http200okresponse.set_data(safxtablesJson)
        print('http200okresponse.__hash__  - get_safxtable:' + str(http200okresponse.__hash__))
        return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


def update_safxcolumn(id):
    print('in update_safxcolumn - id', id)
    safxcolumnsListRaw = request.data
    print('safxcolumnsListRaw:', safxcolumnsListRaw)
    safxcolumnsListBytes = io.BytesIO(safxcolumnsListRaw)
    safxcolumnsList = json.load(safxcolumnsListBytes)
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

def update_safxtable_dstable(id, dsTableId):
    print('in update_safxtable_dstable')
    dsTable = DSTable.select().where(DSTable.id==dsTableId)
    safxTableDic = dict(id=id)
    safxTable = SAFXTable.update(**safxTableDic,dsTable=dsTable)
    safxTable.execute()
    return http200okresponse



