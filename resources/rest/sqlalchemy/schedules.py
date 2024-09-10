import sys
import io
import logging
import json
import datetime

from flask import Response, request, jsonify
from flask_restful import Resource, Api

from sqlalchemy.orm import Session
from sqlalchemy import select, delete, insert, update

from entity import *
from util.util import *

class ScheduleListController(Resource):
    logger = logging.getLogger(__name__ + '.ScheduleListController')
    
    def get(self):
        self.logger.debug('in list_schedules')
        session = Session(engine)
        try: 
            page = int(request.args.get('page'))
            size = int(request.args.get('size'))
            schedulesStt = select(Schedule).limit(size).offset((page)*size)
            schedules = session.scalars(schedulesStt).fetchall()            
            schedulesJson = '{"content": [], "totalPages": 0}'
            if (len(schedules) > 0):
                schedulesAllStt = select(Schedule).limit(size).offset((page)*size)
                schedulesAll = session.scalars(schedulesAllStt).fetchall()            
                count = len(schedulesAll)
                totalPages = int(count / size) + 1 if count % size != 0 else 0
                schedulesJson = wrap(schedules)
            self.logger.debug('schedulesJson:' + schedulesJson)
            return generate_http200ok(schedulesJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


class ScheduleObjectController(Resource):
    logger = logging.getLogger(__name__ + '.ScheduleObjectController')
    
    def post(self):
        self.logger.debug('in insert_update_schedule')
        session = Session(engine)
        scheduleRaw = request.data
        scheduleBytes = io.BytesIO(scheduleRaw)
        schedule = json.load(scheduleBytes)
            
        self.logger.debug('scheduleBytes:' + str(scheduleBytes.getvalue(), encoding='utf-8'))    
        safxTables = []
        for safxTable in schedule['safxTables']:
            safxtablesStt = select(SAFXTable).where(SAFXTable.id==safxTable.get('id'))
            safxTableEntity = session.scalars(safxtablesStt).one()
            safxTables.append(safxTableEntity)
        
        criterias = schedule['criterias'][:] #shallow copy
        if schedule.get('userName') != None:
            del schedule['userName']
        del schedule['safxTables']
        del schedule['criterias']
        newId = None
        if schedule.get('id') == None: #new
            schedule['status'] = 'ACTIVE'
            schedule['lastExecution'] = datetime.datetime.now()
            usersStt = select(User).where(User.id==1)
            user = session.scalars(usersStt).one()
            scheduleInsert = insert(Schedule).values(**schedule, user_id=user.id)
            self.logger.debug('scheduleInsert:')
            self.logger.debug(scheduleInsert)
            result = session.execute(scheduleInsert)
            self.logger.debug('result:')
            self.logger.debug(result)
            newId = result.inserted_primary_key[0]
            self.logger.debug('newId:' + int(newId) + ' - dir' + newId.__class__)
        else:
            scheduleCopy = schedule.copy()
            del scheduleCopy['id']
            scheduleUpdate = update(Schedule).values(**scheduleCopy).where(Schedule.id==schedule.get('id'))
            self.logger.debug('scheduleUpdate:')
            self.logger.debug(scheduleUpdate)
            session.execute(scheduleUpdate) #update
            
        if schedule.get('id') == None:
            schedule['id'] = newId

        scheduleStt = select(Schedule).where(Schedule.id==schedule.get('id'))
        scheduleEntity = session.scalars(scheduleStt).one()
        for safxTable in safxTables:
            associated = False
            for scheduleAssociated in safxTable.schedules:
                if scheduleAssociated.id == scheduleEntity.id:
                    associated = True
            if associated == False:
                safxTable.schedules.append(scheduleEntity)
                session.add(safxTable)

        criteriasToRemove = []
        for criteriaStored in scheduleEntity.criterias:
            criteriasToRemove.append(criteriaStored.id)
        
        for criteria in criterias:
            criteriaQuery = None
            safxColumnId = criteria.get('safxColumn').get('id')

            safxColumnStt = select(SAFXColumn).where(SAFXColumn.id==safxColumnId)
            safxColumn = session.scalars(safxColumnStt).one()

            del criteria['safxColumn']
            if criteria.get('id'):
                criteriasToRemove.remove(criteria.get('id'))
            else:
                criteriaEntity = Criteria(**criteria)
                criteriaEntity.schedule = scheduleEntity
                criteriaEntity.safxColumn = safxColumn
                session.add(criteriaEntity)

        #remove old criterias
        if len(criteriasToRemove) > 0:
            criteriaDeleteQuery = delete(Criteria).where(Criteria.id.in_(criteriasToRemove))
            session.execute(criteriaDeleteQuery)
            #for criteriaId in criteriasToRemove:
            #    criteriaDeleteQuery = delete(Criteria).where(Criteria.id == criteriaId)
            #    session.execute(criteriaDeleteQuery)
                
        session.commit()        
        return generate_http200ok()

    def delete(self, id):
        self.logger.debug('in delete_schedule:' + str(id))
        session = Session(engine)
        schedulesStt = delete(Schedule).where(Schedule.id==id)
        schedule_r = session.execute(schedulesStt)
        session.commit()
        #q = Schedule.delete().where(Schedule.id==id)
        #q.execute()
        return generate_http200ok()


    def get(self, id):
        self.logger.debug('in get_schedule:' + str(id))
        try: 
            session = Session(engine)
            schedulesStt = select(Schedule).where(Schedule.id==id)
            schedules = session.scalars(schedulesStt).fetchall()
            schedule = schedules[0]
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
            session = Session(engine)
            schedulesStt = select(Schedule).where(Schedule.id==id)
            schedules = session.scalars(schedulesStt).fetchall()
            schedule = schedules[0]
            #schedule = Schedule.get(int(id))
            schedulesJson = '{ "days" : "' + schedule.days + '", "hours": "' + schedule.hours + '" } '
            return generate_http200ok(schedulesJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []




