from flask import Response
from werkzeug.datastructures import * #.Headers

GlobalVar = 'WE'

OURheader = Headers()
OURheader.add('access-control-allow-origin', '*')
http200okresponse = Response(
    response='',
    headers=OURheader,
    status=200,
    mimetype='application/json'
)

def wraplist(values):
    vsJson = '['
    for v in values:
        vJson = v.toJson()
        vsJson = vsJson + vJson + ','
    vsJson = vsJson[0:len(vsJson)-1] + ']'
    return vsJson

def wrap(values, totalPages=1):
    vsJson = wraplist(values)
    wrapper = '{"content": ' + vsJson + ', "totalPages": ' + str(totalPages)+ '}'
    return wrapper
