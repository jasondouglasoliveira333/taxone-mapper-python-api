import sys
import io
import json
from flask import Response, request, jsonify
from werkzeug.datastructures import * #.Headers

from entity import *
from util import *

def list_shedules():
    print('in list_shedules')
    try: 
        page = request.args.get('page')
        size = request.args.get('size')
        shedules = Schedule.select()
        shedulesJson = '{"content": [], "totalPages": 0}'
        if (len(shedules) > 0):
            shedulesJson = wrap(shedules)
        print('shedulesJson:', shedulesJson)
        http200okresponse.set_data(shedulesJson)
        return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


def insert_update_schedule():
    print('in insert_update_schedule')
    scheduleRaw = request.data
    scheduleBytes = io.BytesIO(scheduleRaw)
    schedule = json.load(scheduleBytes)
    print ('schedule[\'safxTables\']:', schedule['safxTables'])
    safxTables = []
    for safxTable in schedule['safxTables']:
        safxTableEntity = SAFXTable.get(safxTable.get('id'))
        safxTables.append(safxTableEntity)

    criterias = schedule['criterias'][:] #shallow copy
    del schedule['userName']
    del schedule['safxTables']
    del schedule['criterias']
    scheduleQuery = Schedule.update(**schedule).where(Schedule.id==schedule.get('id'))
    print('scheduleQuery.sql():', scheduleQuery.sql())
    scheduleQuery.execute()
    scheduleEntity = Schedule.get(schedule.get('id'))
    for safxTable in safxTables:
        safxTable.schedule = scheduleEntity
        safxTable.save()

    for criteria in criterias:
        criteriaQuery = None
        print('>>>criteria:', criteria)
        safxColumnId = criteria.get('safxColumn').get('id')
        safxColumn = SAFXColumn.get(safxColumnId)
        print('>>safxColumn:', safxColumn)
        del criteria['safxColumn']
        if criteria.get('id'):
            criteriaQuery = Criteria.update(**criteria, schedule = scheduleEntity, safxColumn=safxColumn).where(Criteria.id == criteria.get('id'))
        else:
            criteriaQuery = Criteria.insert(**criteria, schedule = scheduleEntity, safxColumn=safxColumn)
        print('criteriaQuery.sql():', criteriaQuery.sql())
        criteriaQuery.execute()
        
    return http200okresponse

def delete_shedule(id):
    print('in delete_shedule:', id)
    q = Schedule.delete().where(Schedule.id==id)
    q.execute()
    print('deleted')
    return http200okresponse


def get_schedule(id):
    print('in get_schedule:', id)
    try: 
        schedule = Schedule.get(id)
        schedulesJson = schedule.toJson()
        print('schedulesJson:', schedulesJson)
        http200okresponse.set_data(schedulesJson)
        return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


def get_schedule_periods(id):
    print('in get_schedule:', id)
    try: 
        schedule = Schedule.get(id)
        schedulesJson = '{ "days" : "' + schedule.days + '", "hours": "' + schedule.hours + '" } '
        print('schedulesJson:', schedulesJson)
        http200okresponse.set_data(schedulesJson)
        return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []




