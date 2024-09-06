import sys
import io
import datetime
import json
from flask import Response, request

from entity import *
from util import *

got_metadata = False

def list_data_source_configs():
    print('in list_dataSourceConfigs')
    try: 
        page = request.args.get('page')
        size = request.args.get('size')
        dataSourceConfigs = DataSourceConfiguration.select()
        dataSourceConfigsJson = '{"content": [], "totalPages": 0}'
        print('len(dataSourceConfigs):', len(dataSourceConfigs))
        if (len(dataSourceConfigs) > 0):
            dataSourceConfigsJson = wraplist(dataSourceConfigs)
        print('dataSourceConfigsJson:', dataSourceConfigsJson)
        http200okresponse.set_data(dataSourceConfigsJson)
        return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []
        
def list_dsTables(dataSourceType):
    print('in list_dsTables - dataSourceType:', dataSourceType)
    try: 
        if got_metadata:
            table = 'customer'
            dsTable = DSTable()
            dsTable.id = 1
            dsTable.name = table
            dSTables = []
            dSTables.append(dsTable)
            dSTablesJson = wraplist(dSTables)
            print('dSTablesJson:', dSTablesJson)
            http200okresponse.set_data(dSTablesJson)
            return http200okresponse
        else:
            page = request.args.get('page')
            size = request.args.get('size')
            dSTables = DSTable.select().join(DataSourceConfiguration).where(DataSourceConfiguration.dataSourceType == dataSourceType)
            dSTablesJson = '[]'
            print('len(dSTables):', len(dSTables))
            if (len(dSTables) > 0):
                dSTablesJson = wraplist(dSTables)
            print('dSTablesJson:', dSTablesJson)
            http200okresponse.set_data(dSTablesJson)
            return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []
    
    
def get_metadata(dataSourceType):
    print('in get_metadata:', dataSourceType)
    try:
        dsColumnList = []
        table = 'customer'
        x = 1
        while x < 2:
        #for x in range(1,10):
            dsC = DSColumn()
            dsC.id = x
            dsC.name = 'column_' + str(x) 
            dsC.columnType = 'varchar'
            dsC.size = 255
            dsTable = DSTable()
            dsTable.id = 1
            dsTable.name = table
            dsC.dsTable = dsTable
            dsColumnList.append(dsC)
            x = x + 1
        
        print('>>x')
        dSCsJson = wrap(dsColumnList)
        print('dSCsJson:', dSCsJson)
        http200okresponse.set_data(dSCsJson)
        got_metadata = True
        return http200okresponse
    except:
        print('sys.exception():', repr(sys.exception()))
        return []


def list_dsColumns(dataSourceType, dsTableId):
    return get_metadata(dataSourceType)

def insert_dsConfiguration(dataSourceType):
    print('in insert_dsConfiguration - dataSourceType:', dataSourceType)
    dsConfigRaw = request.data
    print('dsConfigRaw:', dsConfigRaw)
    dsConfigBytes = io.BytesIO(dsConfigRaw)
    dsConfig = json.load(dsConfigBytes)
    dataSourceConfiguration = DataSourceConfiguration.create(**dsConfig)

    #dsTable
    table = 'customer'
    dsTable = DSTable()
    dsTable.name = table
    dsTable.dataSourceConfiguration = dataSourceConfiguration
    dsTable.save()
    
    #column
    dsC = DSColumn()
    dsC.name = 'column_' + str(1) 
    dsC.columnType = 'varchar'
    dsC.size = 255
    dsC.dsTable = dsTable
    dsC.save()
    print('dsC.save()')
    return http200okresponse

def get_data_source_config(dataSourceType):
    print('in get_data_source_config - dataSourceType:', dataSourceType)
    dataSourceConfigurations = DataSourceConfiguration.select().where(DataSourceConfiguration.dataSourceType == dataSourceType)
    dSCJson = '{}'
    if len(dataSourceConfigurations) > 0:
        dataSourceConfiguration = dataSourceConfigurations[0]
        dSCJson = dataSourceConfiguration.toJson()
        
    http200okresponse.set_data(dSCJson)
    return http200okresponse
    