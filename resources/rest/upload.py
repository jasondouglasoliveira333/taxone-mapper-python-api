import sys
import io
import logging
import datetime
import json
from flask import Response, request
from flask_restful import Resource, Api

from entity import *
from util.util import *

class UploadController(Resource):
    logger = logging.getLogger(__name__ + '.UploadController')
    def get(self):
        self.logger.debug('in list_uploads')
        try: 
            page = int(request.args.get('page'))
            size = int(request.args.get('size'))
            uploads = Upload.select().paginate(page+1, size)
            uploadsJson = '{"content": [], "totalPages": 0}'
            self.logger.debug('len(uploads):' + str(len(uploads)))
            if (len(uploads) > 0):
                count = len(Upload.select())
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
            files = request.files['file']
            layoutVersion = request.form.get('layoutVersion')
            users = User.select().where(User.id == 1)
            self.logger.debug('len(users):' + str(len(users)))
            user = users[0]
            self.logger.debug('>>>user.name' + user.name + ' - files.filename:' + files.filename)
            upload = Upload()
            upload.fileName = files.filename
            upload.layoutVersion = layoutVersion #'3'
            upload.creationDate = datetime.datetime.now()
            upload.status = 'ACTIVE'
            upload.user = user
            upload.save()
            self.logger.debug('Saved')
        except:    
            self.logger.debug('sys.exception():' + repr(sys.exception()))
            return []


