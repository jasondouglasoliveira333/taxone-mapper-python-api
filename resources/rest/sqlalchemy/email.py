import sys
import io
import logging
import json

from flask import Response, request, jsonify
from flask_restful import Resource, Api

from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from entity import *
from util import *

class EmailController(Resource):
    logger = logging.getLogger(__name__ + '.EmailController')
    
    def get(self):
        self.logger.debug('in list_emails')
        try: 
            session = Session(engine)
            page = request.args.get('page')
            size = request.args.get('size')
            emailsStt = select(Email)
            emails = session.scalars(emailsStt).fetchall()
            emailsJson = '{"content": [], "totalPages": 0}'
            if (len(emails) > 0):
                emailsJson = wrap(emails)
            self.logger.debug('emailsJson:' + emailsJson)
            http200okresponse.set_data(emailsJson)
            return http200okresponse
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []

    def post(self):
        self.logger.debug('in post')
        session = Session(engine)
        emailsListRaw = request.data
        emailsListBytes = io.BytesIO(emailsListRaw)
        emailsList = json.load(emailsListBytes)
        emailsEntity = []
        for email in emailsList:
            if email.get('id') == None:
                email_to_insert = Email(**email)
                session.add(email_to_insert)
                
        session.commit()        
        return http200okresponse

class EmailByIdController(Resource):
    logger = logging.getLogger(__name__ + '.EmailByIdController')
    
    def delete(self,id):
        self.logger.debug('in delete:' + str(id))
        session = Session(engine)
        emailsStt = delete(Email).where(Email.id==id)
        session.execute(emailsStt)
        session.commit()
        return http200okresponse


