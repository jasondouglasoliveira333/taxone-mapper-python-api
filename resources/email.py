import sys
import io
import json
from flask import Response, request, jsonify
from werkzeug.datastructures import * #.Headers

from entity import *
from util.util import *

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
        return generate_http200ok(emailsJson)
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
    return generate_http200ok()

def delete_email(id):
    print('in delete_email:', id)
    q = Email.delete().where(Email.id==id)
    q.execute()
    print('deleted')
    return generate_http200ok()

