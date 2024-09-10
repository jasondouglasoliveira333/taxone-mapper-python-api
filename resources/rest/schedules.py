import sys
import io
import logging
import json
import datetime
from flask import Response, request, jsonify
from flask_restful import Resource, Api
from werkzeug.datastructures import * #.Headers

from entity import *
from util.util import *

class ScheduleListController(Resource):
    logger = logging.getLogger(__name__ + '.ScheduleListController')
    
    def get(self):
        self.logger.debug('in list_shedules')
        try: 
            page = int(request.args.get('page'))
            size = int(request.args.get('size'))
            shedules = Schedule.select().paginate(page+1, size)
            shedulesJson = '{"content": [], "totalPages": 0}'
            if (len(shedules) > 0):
                count = len(Schedule.select())
                totalPages = int(count / size) + 1 if count % size != 0 else 0
                shedulesJson = wrap(shedules)
            self.logger.debug('shedulesJson:' + shedulesJson)
            return generate_http200ok(shedulesJson)
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
        
        criterias = schedule['criterias'][:] #shallow copy
        if schedule.get('userName') != None:
            del schedule['userName']
        del schedule['safxTables']
        del schedule['criterias']
        if schedule.get('id'):
            scheduleQuery = Schedule.update(**schedule).where(Schedule.id==schedule.get('id'))
        else:
            schedule['status'] = 'ACTIVE'
            schedule['lastExecution'] = datetime.datetime.now()
            users = User.select().where(User.id == 1)
            user = users[0]
            scheduleQuery = Schedule.insert(**schedule,user=user)
        newId = scheduleQuery.execute()
        if schedule.get('id') == None:
            schedule['id'] = newId
        scheduleEntity = Schedule.get(schedule.get('id'))
        for safxTable in safxTables:
            associated = False
            for scheduleAssociated in safxTable.schedules:
                if scheduleAssociated.id == scheduleEntity.id:
                    associated = True
            if associated == False:
                safxTable.schedules.add(scheduleEntity)
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

        #remove old criterias
        if len(criteriasToRemove) > 0:
            criteriaDeleteQuery = Criteria.delete().where(Criteria.id.in_(criteriasToRemove))
            criteriaDeleteQuery.execute()
        
        return generate_http200ok()

    def delete(self, id):
        self.logger.debug('in delete_shedule:' + str(id))
        q = Schedule.delete().where(Schedule.id==id)
        q.execute()
        return generate_http200ok()

    def get(self, id):
        self.logger.debug('in get_schedule:' + str(id))
        try: 
            schedule = Schedule.get(int(id))
            schedulesJson = schedule.toJson()
            return generate_http200ok(schedulesJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []

class SchedulePeriodsController(Resource):
    logger = logging.getLogger(__name__ + '.SchedulePeriodsController')
    
    def get(self, id):
        self.logger.debug('in get_schedule_period:' + str(id))
        try: 
            schedule = Schedule.get(int(id))
            schedulesJson = '{ "days" : "' + schedule.days + '", "hours": "' + schedule.hours + '" } '
            return generate_http200ok(schedulesJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []




