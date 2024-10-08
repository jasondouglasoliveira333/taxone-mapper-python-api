import sys
import io
import logging
import datetime
import json
from flask import Response, request
from flask_restful import Resource, Api

from sqlalchemy.orm import Session
from sqlalchemy import select

from entity import *
from util.util import *

got_metadata = False

class DataSourceConfigsController(Resource):
    logger = logging.getLogger(__name__ + '.DataSourceConfigsController')
    
    def get(self):
        self.logger.debug('in list_dataSourceConfigs')
        try: 
            session = Session(engine)
            dataSourceConfigurationsStt = select(DataSourceConfiguration)
            dataSourceConfigs = session.scalars(dataSourceConfigurationsStt).fetchall()
            dataSourceConfigsJson = '[]'
            self.logger.debug('len(dataSourceConfigs):' + str(len(dataSourceConfigs)))
            if (len(dataSourceConfigs) > 0):
                dataSourceConfigsJson = wraplist(dataSourceConfigs)
            self.logger.debug('dataSourceConfigsJson:' + dataSourceConfigsJson)
            return generate_http200ok(dataSourceConfigsJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []
            

class DataSourceConfigsDSTableController(Resource):
    logger = logging.getLogger(__name__ + '.DataSourceConfigsDSTableController')
    
    def get(self, dataSourceType):
        self.logger.debug('in list_dsTables - dataSourceType:' + dataSourceType)
        try: 
            session = Session(engine)
            if got_metadata:
                table = 'customer'
                dsTable = DSTable()
                dsTable.id = 1
                dsTable.name = table
                dSTables = []
                dSTables.append(dsTable)
                dSTablesJson = wraplist(dSTables)
                self.logger.debug('dSTablesJson:' + dSTablesJson)
                return generate_http200ok(dSTablesJson)
            else:
                dsTablesStt = select(DSTable).join(DataSourceConfiguration).where(DataSourceConfiguration.dataSourceType == dataSourceType)
                dSTables = session.scalars(dsTablesStt).fetchall()
                #dSTables = DSTable.select().join(DataSourceConfiguration).where(DataSourceConfiguration.dataSourceType == dataSourceType)
                dSTablesJson = '[]'
                self.logger.debug('len(dSTables):' + str(len(dSTables)))
                if (len(dSTables) > 0):
                    dSTablesJson = wraplist(dSTables)
                self.logger.debug('dSTablesJson:' + dSTablesJson)
                return generate_http200ok(dSTablesJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


class DataSourceConfigsDSColumnsController(Resource):
    def get(self, dataSourceType, dsTableId):
        return DataSourceConfigsMetadataController().post(dataSourceType)


class DataSourceConfigsMetadataController(Resource):
    logger = logging.getLogger(__name__ + '.DataSourceConfigsMetadataController')
    
    def post(self, dataSourceType):
        self.logger.debug('in get_metadata:' + dataSourceType)
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
            
            self.logger.debug('>>x')
            dSCsJson = wrap(dsColumnList)
            self.logger.debug('dSCsJson:' + dSCsJson)
            return generate_http200ok(dSCsJson)
            got_metadata = True
        except:
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


class DataSourceConfigsObjectController(Resource):
    logger = logging.getLogger(__name__ + '.DataSourceConfigsObjectController')
    
    def get(self, dataSourceType):
        self.logger.debug('in get_data_source_config - dataSourceType:' + dataSourceType)
        session = Session(engine)
        dataSourceConfigurationsStt = select(DataSourceConfiguration).where(DataSourceConfiguration.dataSourceType == dataSourceType)
        dataSourceConfigurations = session.scalars(dataSourceConfigurationsStt).fetchall()
        #dataSourceConfigurations = DataSourceConfiguration.select().where(DataSourceConfiguration.dataSourceType == dataSourceType)
        dSCJson = '{}'
        if len(dataSourceConfigurations) > 0:
            dataSourceConfiguration = dataSourceConfigurations[0]
            dSCJson = dataSourceConfiguration.toJson()
            
        return generate_http200ok(dSCJson)
        
    def post(self, dataSourceType):
        self.logger.debug('in insert_dsConfiguration - dataSourceType:' + dataSourceType)
        session = Session(engine)
        dsConfigRaw = request.data
        dsConfigBytes = io.BytesIO(dsConfigRaw)
        dsConfig = json.load(dsConfigBytes)
        dataSourceConfiguration = DataSourceConfiguration(**dsConfig)

        #dsTable
        table = 'customer'
        dsTable = DSTable()
        dsTable.name = table
        dsTable.dataSourceConfiguration = dataSourceConfiguration
        
        #column
        dsC = DSColumn()
        dsC.name = 'column_' + str(1) 
        dsC.columnType = 'varchar'
        dsC.size = 255
        dsC.dsTable = dsTable
        
        session.add_all([dataSourceConfiguration,dsTable,dsC])
        session.commit()
        
        self.logger.debug('dsC.save()')
        return generate_http200ok()
        