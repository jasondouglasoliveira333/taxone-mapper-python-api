import sys
import io
import json
from flask import Response, request, jsonify
from werkzeug.datastructures import * #.Headers

from entity import *
from util import *

def list_emails():
    print('in list_emails')
    try: 
        page = request.args.get('page')
        size = request.args.get('size')
        emails = Email.select()
        emailsJson = '{"content": [], "totalPages": 0}'
        if (len(emails) > 0):
            emailsJson = wrap(emails)
        print('emailsJson:', emailsJson)
        http200okresponse.set_data(emailsJson)
        return http200okresponse
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


def insert_update_email():
    print('in insert_update_email')
    emailsListRaw = request.data
    emailsListBytes = io.BytesIO(emailsListRaw)
    emailsList = json.load(emailsListBytes)
    emailsEntity = []
    for email in emailsList:
        if email.get('id'):
            Email.update(**email)
        else:
            Email.create(**email)
    return http200okresponse

def delete_email(id):
    print('in delete_email:', id)
    q = Email.delete().where(Email.id==id)
    q.execute()
    print('deleted')
    return http200okresponse

