import sys
import io
import datetime
import json
from flask import Response, request

from entity import *
from util.util import *

def list_uploads():
    print('in list_uploads')
    try: 
        page = request.args.get('page')
        size = request.args.get('size')
        uploads = Upload.select()
        uploadsJson = '{"content": [], "totalPages": 0}'
        print('len(uploads):', len(uploads))
        if (len(uploads) > 0):
            uploadsJson = wrap(uploads)
        print('uploadsJson:', uploadsJson)
        return generate_http200ok(uploadsJson)
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []
        
def insert_upload():
    try: 
        print('in insert_upload', request.files)
        files = request.files['file']
        #print('files', dir(files))
        layoutVersion = request.form.get('layoutVersion')
        users = User.select().where(User.id == 1)
        print('len(users):', len(users))
        user = users[0]
        print('>>>user.name', user.name, ' - files.filename:', files.filename)
        upload = Upload()
        upload.fileName = files.filename
        upload.layoutVersion = layoutVersion #'3'
        upload.creationDate = datetime.datetime.now()
        upload.status = 'ACTIVE'
        upload.user = user
        upload.save()
        print('Saved')
    except:    
        print('sys.exception():', repr(sys.exception()))
        return []


