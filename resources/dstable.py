import sys
import io
import json
from flask import Response, request, jsonify
from werkzeug.datastructures import * #.Headers

from entity import *
from util import *

def list_dstables():
    print('in list_dstables')
    try: 
        dstables = DSTable.select()
        dstablesJson = '[]'
        if (len(dstables) > 0):
            dstablesJson = wraplist(dstables)
        print('dstablesJson:', dstablesJson)
        http200okresponse.set_data(dstablesJson)
        return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


def list_dsTable_dsColumns(id):
    print('in list_dsTable_dsColumns')
    try: 
        dscolumns = DSColumn.select().join(DSTable).where(DSTable.id==id)
        #print('dscolumns.sql()', dscolumns.sql())
        dscolumnsJson = '{"content": [], "totalPages": 0}'
        if (len(dscolumns) > 0):
            dscolumnsJson = wrap(dscolumns)
        print('dscolumnsJson:', dscolumnsJson)
        http200okresponse.set_data(dscolumnsJson)
        return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []
    