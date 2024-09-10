import sys
import io
import json
from flask import Response, request, jsonify
from werkzeug.datastructures import * #.Headers

from entity import *
from util.util import *

def list_schedulelogs():
    print('in list_schedulelogs:')
    try: 
        page = request.args.get('page')
        size = request.args.get('size')
        status = request.args.get('status')
        schedulelogs = ScheduleLog.select().where(ScheduleLog.status==status)
        schedulelogsJson = '{"content": [], "totalPages": 0}'
        if (len(schedulelogs) > 0):
            schedulelogsJson = wrap(schedulelogs)
        print('schedulelogsJson:', schedulelogsJson)
        return generate_http200ok(schedulelogsJson)
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []

def list_schedulelog_statistics():
    print('in list_schedulelogs:')
    try: 
        schedulelogs = ScheduleLog.select()
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
        print('sys.exception():', repr(sys.exception()))
        return []

