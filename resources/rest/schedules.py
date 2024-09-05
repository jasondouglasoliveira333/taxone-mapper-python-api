import sys
import io
import logging
import json
from flask import Response, request, jsonify
from flask_restful import Resource, Api
from werkzeug.datastructures import * #.Headers

from entity import *
from util import *

logger = logging.getLogger(__name__)

class ScheduleListController(Resource):
    def get(self):
        logger.info('in list_shedules')
        try: 
            page = request.args.get('page')
            size = request.args.get('size')
            shedules = Schedule.select()
            shedulesJson = '{"content": [], "totalPages": 0}'
            if (len(shedules) > 0):
                shedulesJson = wrap(shedules)
            #logger.info('shedulesJson:', shedulesJson)
            http200okresponse.set_data(shedulesJson)
            return http200okresponse
        except:    
            logger.info('sys.exception():' + repr(sys.exception()))
            return []


class ScheduleObjectController(Resource):
    def post(self):
        logger.info('in insert_update_schedule')
        scheduleRaw = request.data
        scheduleBytes = io.BytesIO(scheduleRaw)
        schedule = json.load(scheduleBytes)
            
        logger.info('scheduleBytes:' + str(scheduleBytes.getvalue(), encoding='utf-8'))    
        safxTables = []
        for safxTable in schedule['safxTables']:
            safxTableEntity = SAFXTable.get(safxTable.get('id'))
            safxTables.append(safxTableEntity)
        
        logger.info('>>>schedule[\'criterias\']:')
        logger.info(schedule['criterias'])
        criterias = schedule['criterias'][:] #shallow copy
        del schedule['userName']
        del schedule['safxTables']
        del schedule['criterias']
        scheduleQuery = Schedule.update(**schedule).where(Schedule.id==schedule.get('id'))
        #logger.info('scheduleQuery.sql():', scheduleQuery.sql())
        scheduleQuery.execute()
        scheduleEntity = Schedule.get(schedule.get('id'))
        for safxTable in safxTables:
            safxTable.schedule = scheduleEntity
            safxTable.save()

        criteriasToRemove = []
        for criteriaStored in scheduleEntity.criterias:
            criteriasToRemove.append(criteriaStored.id)
        
        for criteria in criterias:
            criteriaQuery = None
            safxColumnId = criteria.get('safxColumn').get('id')
            safxColumn = SAFXColumn.get(SAFXColumn.id==safxColumnId)
            del criteria['safxColumn']
            if criteria.get('id'):
                criteriasToRemove.remove(criteria.get('id'))
            else:
                criteriaQuery = Criteria.insert(**criteria, schedule = scheduleEntity, safxColumn=safxColumn)
                criteriaQuery.execute()
                logger.info('criteriaQuery.sql():' + criteriaQuery.sql())

        #remove old criterias
        if len(criteriasToRemove) > 0:
            criteriaDeleteQuery = Criteria.delete().where(Criteria.id.in_(criteriasToRemove))
            logger.info('criteriaDeleteQuery.sql():')
            logger.info(criteriaDeleteQuery.sql())
            criteriaDeleteQuery.execute()
        return http200okresponse

    def delete(self, id):
        logger.info('in delete_shedule:', id)
        q = Schedule.delete().where(Schedule.id==id)
        q.execute()
        logger.info('deleted')
        return http200okresponse


    def get(self, id):
        logger.info('in get_schedule:' + str(id))
        try: 
            schedule = Schedule.get(id)
            schedulesJson = schedule.toJson()
            logger.info('schedulesJson:' + schedulesJson)
            http200okresponse.set_data(schedulesJson)
            return http200okresponse
        except:    
            logger.info('sys.exception():' + repr(sys.exception()))
            return []

class SchedulePeriodsController(Resource):
    def get(self, id):
        logger.info('in get_schedule_period:' + str(id))
        try: 
            schedule = Schedule.get(id)
            schedulesJson = '{ "days" : "' + schedule.days + '", "hours": "' + schedule.hours + '" } '
            logger.info('schedulesJson:' + schedulesJson)
            http200okresponse.set_data(schedulesJson)
            return http200okresponse
        except:    
            logger.info('sys.exception():' + repr(sys.exception()))
            return []




