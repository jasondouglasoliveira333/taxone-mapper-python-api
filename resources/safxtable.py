import sys
import io
import json
from flask import Response, request, jsonify
from werkzeug.datastructures import * #.Headers

from entity import *
from util.util import *

def list_safxtables():
    print('in list_safxtables')
    try: 
        page = request.args.get('page')
        size = request.args.get('size')
        safxtables = SAFXTable.select()
        safxtablesJson = '{"content": [], "totalPages": 0}'
        if (len(safxtables) > 0):
            safxtablesJson = wrap(safxtables)
        print('safxtablesJson:', safxtablesJson)
        return generate_http200ok(safxtablesJson)
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
    return generate_http200ok()


def list_safxcoluimns(id):
    print('in list_safxcoluimns')
    try: 
        page = request.args.get('page')
        size = request.args.get('size')
        safxcolumns = SAFXColumn.select().join(SAFXTable).where(SAFXTable.id==id)
        safxcolumnsJson = '[]'
        if (len(safxcolumns) > 0):
            safxcolumnsJson = wraplist(safxcolumns)
        print('safxcolumnsJson:', safxcolumnsJson)
        return generate_http200ok(safxcolumnsJson)
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


def get_safxtable(id):
    print('in get_safxtable:', id)
    try: 
        safxtable = SAFXTable.get(id)
        safxtablesJson = safxtable.toJson()
        print('safxtablesJson:', safxtablesJson)
        return generate_http200ok(safxtablesJson)
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
            
    return generate_http200ok()

def update_safxtable_dstable(id, dsTableId):
    print('in update_safxtable_dstable')
    dsTable = DSTable.select().where(DSTable.id==dsTableId)
    safxTable = SAFXTable.update(dsTable=dsTable).where(SAFXTable.id == id)
    print('safxTable.sql():', safxTable.sql())
    safxTable.execute()
    return generate_http200ok()



