import sys
import io
import logging
import datetime
import json
from flask import Response, request
from flask_restful import Resource, Api

from entity import *
from util.util import *
from resources.integration.placeholder import *

from sqlalchemy.orm import Session
from sqlalchemy import select

class UploadController(Resource):
    logger = logging.getLogger(__name__ + '.UploadController')
    def get(self):
        self.logger.debug('in list_uploads')
        """
        ph = PlaceHolderClient()
        print('will call ph.get_something()')
        ph.get_something()
        print('called ph.get_something()')
        print('will call ph.delete_something()')
        ph.delete_something()
        print('called ph.delete_something()')
        print('will call ph.post_something()')
        ph.post_something()
        print('called ph.post_something()')
        print('will call ph.update_something()')
        ph.update_something()
        print('called ph.update_something()')
        """
        session = Session(engine)
        try: 
            page = int(request.args.get('page'))
            size = int(request.args.get('size'))
            uploadsStt = select(Upload).limit(size).offset((page)*size)
            uploads = session.scalars(uploadsStt).fetchall()
            uploadsJson = '{"content": [], "totalPages": 0}'
            self.logger.debug('len(uploads):' + str(len(uploads)))
            if (len(uploads) > 0):
                uploadsAllStt = select(Upload)
                uploadsAll = session.scalars(uploadsAllStt).fetchall()
                count = len(uploadsAll)
                totalPages = int(count / size) + 1 if count % size != 0 else 0
                uploadsJson = wrap(uploads, totalPages)
            self.logger.debug('uploadsJson:' + uploadsJson)
            return generate_http200ok(uploadsJson)
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
            return generate_http200ok()
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


