import sys
import io
import logging
import json
from flask import Response, request, jsonify
from flask_restful import Resource, Api
from werkzeug.datastructures import * #.Headers

from entity import *
from util import *

class ScheduleListController(Resource):
    logger = logging.getLogger(__name__ + '.ScheduleListController')
    
    def get(self):
        self.logger.debug('in list_shedules')
        try: 
            page = request.args.get('page')
            size = request.args.get('size')
            shedules = Schedule.select()
            shedulesJson = '{"content": [], "totalPages": 0}'
            if (len(shedules) > 0):
                shedulesJson = wrap(shedules)
            self.logger.debug('shedulesJson:' + shedulesJson)
            http200okresponse.set_data(shedulesJson)
            return http200okresponse
        except:    
            logger.debug('sys.exception():' + repr(sys.exception()))
            return []


class ScheduleObjectController(Resource):
    logger = logging.getLogger(__name__ + '.ScheduleObjectController')
    
    def post(self):
        self.logger.debug('in insert_update_schedule')
        scheduleRaw = request.data
        scheduleBytes = io.BytesIO(scheduleRaw)
        schedule = json.load(scheduleBytes)
            
        self.logger.debug('scheduleBytes:' + str(scheduleBytes.getvalue(), encoding='utf-8'))    
        safxTables = []
        for safxTable in schedule['safxTables']:
            safxTableEntity = SAFXTable.get(safxTable.get('id'))
            safxTables.append(safxTableEntity)
        
        self.logger.debug('>>>schedule[\'criterias\']:')
        self.logger.debug(schedule['criterias'])
        criterias = schedule['criterias'][:] #shallow copy
        del schedule['userName']
        del schedule['safxTables']
        del schedule['criterias']
        scheduleQuery = Schedule.update(**schedule).where(Schedule.id==schedule.get('id'))
        self.logger.debug('scheduleQuery.sql():')
        self.logger.debug(scheduleQuery.sql())
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
                self.logger.debug('criteriaQuery.sql():')
                self.logger.debug(criteriaQuery.sql())

        #remove old criterias
        if len(criteriasToRemove) > 0:
            criteriaDeleteQuery = Criteria.delete().where(Criteria.id.in_(criteriasToRemove))
            self.logger.debug('criteriaDeleteQuery.sql():')
            self.logger.debug(criteriaDeleteQuery.sql())
            criteriaDeleteQuery.execute()
        return http200okresponse

    def delete(self, id):
        self.logger.debug('in delete_shedule:' + str(id))
        q = Schedule.delete().where(Schedule.id==id)
        q.execute()
        self.logger.debug('deleted')
        return http200okresponse


    def get(self, id):
        self.logger.debug('in get_schedule:' + str(id))
        try: 
            schedule = Schedule.get(id)
            schedulesJson = schedule.toJson()
            self.logger.debug('schedulesJson:' + schedulesJson)
            http200okresponse.set_data(schedulesJson)
            return http200okresponse
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []

class SchedulePeriodsController(Resource):
    logger = logging.getLogger(__name__ + '.SchedulePeriodsController')
    
    def get(self, id):
        self.logger.debug('in get_schedule_period:' + str(id))
        try: 
            schedule = Schedule.get(id)
            schedulesJson = '{ "days" : "' + schedule.days + '", "hours": "' + schedule.hours + '" } '
            self.logger.debug('schedulesJson:' + schedulesJson)
            http200okresponse.set_data(schedulesJson)
            return http200okresponse
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []




