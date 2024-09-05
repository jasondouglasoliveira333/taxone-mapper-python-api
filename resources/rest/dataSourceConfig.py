import sys
import io
import logging
import datetime
import json
from flask import Response, request
from flask_restful import Resource, Api

from entity import *
from util import *

got_metadata = False

class DataSourceConfigsController(Resource):
    logger = logging.getLogger(__name__ + '.DataSourceConfigsController')
    def get(self):
        self.logger.info('in list_dataSourceConfigs')
        try: 
            page = request.args.get('page')
            size = request.args.get('size')
            dataSourceConfigs = DataSourceConfiguration.select()
            dataSourceConfigsJson = '{"content": [], "totalPages": 0}'
            self.logger.info('len(dataSourceConfigs):' + str(len(dataSourceConfigs)))
            if (len(dataSourceConfigs) > 0):
                dataSourceConfigsJson = wraplist(dataSourceConfigs)
            self.logger.info('dataSourceConfigsJson:' + dataSourceConfigsJson)
            http200okresponse.set_data(dataSourceConfigsJson)
            return http200okresponse
        except:    
            self.logger.info('sys.exception():' + repr(sys.exception()))
            return []
            

class DataSourceConfigsDSTableController(Resource):
    logger = logging.getLogger(__name__ + '.DataSourceConfigsDSTableController')
    def get(self, dataSourceType):
        self.logger.info('in list_dsTables - dataSourceType:' + dataSourceType)
        try: 
            if got_metadata:
                table = 'customer'
                dsTable = DSTable()
                dsTable.id = 1
                dsTable.name = table
                dSTables = []
                dSTables.append(dsTable)
                dSTablesJson = wraplist(dSTables)
                self.logger.info('dSTablesJson:' + dSTablesJson)
                http200okresponse.set_data(dSTablesJson)
                return http200okresponse
            else:
                page = request.args.get('page')
                size = request.args.get('size')
                dSTables = DSTable.select().join(DataSourceConfiguration).where(DataSourceConfiguration.dataSourceType == dataSourceType)
                dSTablesJson = '[]'
                self.logger.info('len(dSTables):' + str(len(dSTables)))
                if (len(dSTables) > 0):
                    dSTablesJson = wraplist(dSTables)
                self.logger.info('dSTablesJson:' + dSTablesJson)
                http200okresponse.set_data(dSTablesJson)
                return http200okresponse
        except:    
            self.logger.info('sys.exception():' + repr(sys.exception()))
            return []


class DataSourceConfigsDSColumnsController(Resource):
    def get(self, dataSourceType, dsTableId):
        return DataSourceConfigsMetadataController().post(dataSourceType)


class DataSourceConfigsMetadataController(Resource):
    logger = logging.getLogger(__name__ + '.DataSourceConfigsMetadataController')
    def post(self, dataSourceType):
        self.logger.info('in get_metadata:' + dataSourceType)
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
            
            self.logger.info('>>x')
            dSCsJson = wrap(dsColumnList)
            self.logger.info('dSCsJson:' + dSCsJson)
            http200okresponse.set_data(dSCsJson)
            got_metadata = True
            return http200okresponse
        except:
            self.logger.info('sys.exception():' + repr(sys.exception()))
            return []


class DataSourceConfigsObjectController(Resource):
    logger = logging.getLogger(__name__ + '.DataSourceConfigsObjectController')
    def get(self, dataSourceType):
        self.logger.info('in get_data_source_config - dataSourceType:' + dataSourceType)
        dataSourceConfigurations = DataSourceConfiguration.select().where(DataSourceConfiguration.dataSourceType == dataSourceType)
        dSCJson = '{}'
        if len(dataSourceConfigurations) > 0:
            dataSourceConfiguration = dataSourceConfigurations[0]
            dSCJson = dataSourceConfiguration.toJson()
            
        http200okresponse.set_data(dSCJson)
        return http200okresponse
        
    def post(self, dataSourceType):
        self.logger.info('in insert_dsConfiguration - dataSourceType:' + dataSourceType)
        dsConfigRaw = request.data
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
        self.logger.info('dsC.save()')
        return http200okresponse

        