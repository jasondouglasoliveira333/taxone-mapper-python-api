import sys
import io
import json
import logging
from datetime import datetime

from flask import Response, request, jsonify
from flask_restful import Resource, Api

from sqlalchemy import select
from sqlalchemy.orm import Session 
from sqlalchemy.sql import text

from entity import *
from util.util import *

class ScheduleLogListController(Resource):
    logger = logging.getLogger(__name__ + '.ScheduleLogListController')
    
    def get(self):
        self.logger.debug('in list_schedulelogs_list_x:')
        try: 
            session = Session(engine)
            page = int(request.args.get('page'))
            size = int(request.args.get('size'))
            status = request.args.get('status')
            schedulelogsStt = select(ScheduleLog).where(ScheduleLog.status==status).limit(size).offset((page)*size)
            schedulelogs = session.scalars(schedulelogsStt).fetchall()
            schedulelogsJson = '{"content": [], "totalPages": 0}'
            if (len(schedulelogs) > 0):
                schedulelogsAllStt = select(ScheduleLog).where(ScheduleLog.status==status)
                schedulelogsAll = session.scalars(schedulelogsAllStt).fetchall()
                count = len(schedulelogsAll)
                totalPages = int(count / size) + 1 if count % size != 0 else 0
                schedulelogsJson = wrap(schedulelogs, totalPages)
            self.logger.debug('schedulelogsJson:' + schedulelogsJson)
            return generate_http200ok(schedulelogsJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []

class ScheduleLogStatisticsController(Resource):
    logger = logging.getLogger(__name__ + '.ScheduleLogStatisticsController')
    
    def get(self):
        self.logger.debug('in list_schedulelogs_statistics:')
        try: 
            session = Session(engine)
            schedulelogsStt = select(ScheduleLog)
            schedulelogs = session.scalars(schedulelogsStt).fetchall()
            PROCESSED = 0
            PROCESSING = 0
            ERROR_TAXONE = 0
            for schedulelog in schedulelogs:
                match schedulelog.status:
                    case 'PROCESSED':
                        PROCESSED = PROCESSED + 1
                    case 'PROCESSING':
                        PROCESSING = PROCESSING + 1
                    case 'ERROR_TAXONE':
                        ERROR_TAXONE = ERROR_TAXONE + 1
            statistics = []
            statistics.append({'status':'PROCESSED', 'quantity': PROCESSED})
            statistics.append({'status':'PROCESSING', 'quantity': PROCESSING})
            statistics.append({'status':'ERROR_TAXONE', 'quantity': ERROR_TAXONE})
            statistics.append({'status':'SENT', 'quantity': 0})
            statistics.append({'status':'PROCESSING_ERROR', 'quantity': 0})
            statisticsJson = json.dumps(statistics)
            return generate_http200ok(statisticsJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


class ScheduleLogObjectController(Resource):
    logger = logging.getLogger(__name__ + '.ScheduleLogObjectController')
    
    def get(self, id):
        self.logger.debug('in get_schedulelog:' + str(id))
        try: 
            session = Session(engine)
            schedulelogsStt = select(ScheduleLog).where(ScheduleLog.id==id)
            scheduleLog = session.scalars(schedulelogsStt).one()
            scheduleLogsJson = scheduleLog.toJson()
            self.logger.debug('scheduleLogsJson:' + scheduleLogsJson)
            return generate_http200ok(scheduleLogsJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


class ScheduleLogTaxOneErrorController(Resource):
    logger = logging.getLogger(__name__ + '.ScheduleLogTaxOneErrorController')
        
    def get(self, id):
        self.logger.debug('in get_schedulelog_taxoneerror:' + str(id))
        try: 
            session = Session(engine)
            schedulelogsStt = select(ScheduleLog).where(ScheduleLog.id==int(id))
            scheduleLog = session.scalars(schedulelogsStt).one()
            taxOneErrorsJson = '{"content": [], "totalPages": 0}'
            if (len(scheduleLog.taxOneErrors) > 0):
                taxOneErrorsJson = wrap(scheduleLog.taxOneErrors)
            self.logger.debug('taxOneErrorsJson:' + taxOneErrorsJson)
            return generate_http200ok(taxOneErrorsJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []




#            schedulesRaw = session.execute(text('select * from schedule')).fetchall()
#            for s in schedulesRaw:
#                print('s:', s, ' - class:', s.__class__)

