import sys
import io
import json
from flask import Response, request, jsonify
from werkzeug.datastructures import * #.Headers

from entity import *
from util.util import *

def list_shedules():
    print('in list_shedules')
    try: 
        page = request.args.get('page')
        size = request.args.get('size')
        shedules = Schedule.select()
        shedulesJson = '{"content": [], "totalPages": 0}'
        if (len(shedules) > 0):
            shedulesJson = wrap(shedules)
        return generate_http200ok(shedulesJson)
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


def insert_update_schedule():
    print('in insert_update_schedule')
    scheduleRaw = request.data
    scheduleBytes = io.BytesIO(scheduleRaw)
    schedule = json.load(scheduleBytes)
        
    print('scheduleBytes:' + str(scheduleBytes.getvalue(), encoding='utf-8'))    
    safxTables = []
    for safxTable in schedule['safxTables']:
        safxTableEntity = SAFXTable.get(safxTable.get('id'))
        safxTables.append(safxTableEntity)
    
    criterias = schedule['criterias'][:] #shallow copy
    del schedule['userName']
    del schedule['safxTables']
    del schedule['criterias']
    scheduleQuery = Schedule.update(**schedule).where(Schedule.id==schedule.get('id'))
    scheduleQuery.execute()
    scheduleEntity = Schedule.get(schedule.get('id'))
    for safxTable in safxTables:
        associated = False
        for scheduleAssociated in safxTable.schedules:
            if scheduleAssociated.id == scheduleEntity.id:
                associated = True
        if associated == False:
            safxTable.schedules.add(scheduleEntity)
            safxTable.save()
            
    t = TestAdd()
    t.schedule = scheduleEntity
    print('>>>t:', dir(t))

    for criteria in criterias:
        criteriaQuery = None
        safxColumnId = criteria.get('safxColumn').get('id')
        safxColumn = SAFXColumn.get(SAFXColumn.id==safxColumnId)
        del criteria['safxColumn']
        if criteria.get('id'):
            criteriaQuery = Criteria.update(**criteria, schedule = scheduleEntity, safxColumn=safxColumn).where(Criteria.id == criteria.get('id'))
        else:
            criteriaQuery = Criteria.insert(**criteria, schedule = scheduleEntity, safxColumn=safxColumn)
        criteriaQuery.execute()
        
    return generate_http200ok()

class TestAdd(object):
    pass

def delete_shedule(id):
    print('in delete_shedule:', id)
    q = Schedule.delete().where(Schedule.id==id)
    q.execute()
    return generate_http200ok()


def get_schedule(id):
    print('in get_schedule:', id)
    try: 
        schedule = Schedule.get(int(id))
        schedulesJson = schedule.toJson()
        return generate_http200ok(schedulesJson)
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


def get_schedule_periods(id):
    print('in get_schedule:', id)
    try: 
        schedule = Schedule.get(int(id))
        schedulesJson = '{ "days" : "' + schedule.days + '", "hours": "' + schedule.hours + '" } '
        return generate_http200ok(schedulesJson)
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []




