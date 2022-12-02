import traceback
from flask import jsonify, make_response, send_from_directory
from flask_restx import fields, Resource
from json import JSONEncoder
from datetime import date, datetime

from context import swagger
from log import logger

##################################################
# REST API related definitions
##################################################


class ISerializable:
    '''serializable interface
    '''
    pass


class AppJSONEncoder(JSONEncoder):
    '''json encoder for serialization
    '''
    def default(self, obj):
        if isinstance(obj, (ISerializable)):
            return obj.__dict__
        if isinstance(obj, (date, datetime)):
            return obj.__str__()
        return JSONEncoder.default(self, obj)


def request_handle(func):
    '''
    decorator for generic error handling
    '''
    def handle(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
        except Exception as e:
            resp = Response(500, 'Internal Server Error', {})
            error_detail = traceback.format_exc()
            logger.error('\n' + error_detail)
            resp.data['error_detail'] = str(e)
            # resp.data['error_detail'] = error_detail.strip().split('\n')
        finally:
            return make_response(jsonify(resp), resp.status)

    handle.__name__ = func.__name__
    return handle


class Response(ISerializable):
    '''base response class
    '''
    def __init__(self, status=200, msg='success', data=None):
        self.status = status
        self.msg = msg
        self.data = data


# base response api docs
response_model = swagger.model('Response', {
    'status': fields.Integer(description='response status'),
    'msg': fields.String(description='response message'),
    'data': fields.Raw
})


@swagger.response(200, 'ok', model=response_model)
@swagger.response(500, 'error', model=response_model)
class BaseResource(Resource):
    '''base rest api router class
    '''
    pass
