import sys
import io
import logging
import json
from flask import Response, request, jsonify
from flask_restful import Resource, Api
from werkzeug.datastructures import * #.Headers

from entity import *
from util.util import *

class EmailController(Resource):
    logger = logging.getLogger(__name__ + '.EmailController')
    
    def get(self):
        self.logger.debug('in list_emails')
        try: 
            page = request.args.get('page')
            size = request.args.get('size')
            emails = Email.select()
            emailsJson = '{"content": [], "totalPages": 0}'
            if (len(emails) > 0):
                emailsJson = wrap(emails)
            self.logger.debug('emailsJson:' + emailsJson)
            #response = json.loads(emailsJson)
            #self.logger.debug('>>response loaded', response)
            #return response
            return generate_http200ok(emailsJson)
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []

    def post(self):
        self.logger.debug('in post')
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

class EmailByIdController(Resource):
    logger = logging.getLogger(__name__ + '.EmailByIdController')
    
    def delete(self,id):
        self.logger.debug('in delete:' + str(id))
        q = Email.delete().where(Email.id==id)
        q.execute()
        return generate_http200ok()

