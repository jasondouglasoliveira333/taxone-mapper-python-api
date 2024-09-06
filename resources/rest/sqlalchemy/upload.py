import sys
import io
import logging
import datetime
import json
from flask import Response, request
from flask_restful import Resource, Api

from entity import *
from util import *

from sqlalchemy.orm import Session
from sqlalchemy import select

class UploadController(Resource):
    logger = logging.getLogger(__name__ + '.UploadController')
    def get(self):
        self.logger.debug('in list_uploads')
        session = Session(engine)
        try: 
            page = int(request.args.get('page'))
            size = int(request.args.get('size'))
            uploadsStt = select(Upload)
            uploads = session.scalars(uploadsStt).fetchall()
            #print('uploads', dir(uploads))
            uploadsJson = '{"content": [], "totalPages": 0}'
            self.logger.debug('len(uploads):' + str(len(uploads)))
            if (len(uploads) > 0):
                count = len(uploads) #len(Upload.select())
                totalPages = int(count / size) + 1 if count % size != 0 else 0
                uploadsJson = wrap(uploads, totalPages)
            self.logger.debug('uploadsJson:' + uploadsJson)
            http200okresponse.set_data(uploadsJson)
            return http200okresponse
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []
            
    def post(self):
        try: 
            self.logger.debug('in insert_upload')
            self.logger.debug(request.files)
            session = Session(engine)
            files = request.files['file']
            layoutVersion = request.form.get('layoutVersion')
            usersStt = select(User).where(User.id == 1)
            users = session.scalars(usersStt).fetchall()
            user = users[0]
            self.logger.debug('>>>user.name' + user.name + ' - files.filename:' + files.filename)
            upload = Upload()
            upload.fileName = files.filename
            upload.layoutVersion = layoutVersion #'3'
            upload.creationDate = datetime.datetime.now()
            upload.status = 'ACTIVE'
            upload.user = user
            #upload.save()
            session.add(upload)
            session.commit()
            self.logger.debug('Saved')
            return http200okresponse
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


