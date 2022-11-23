from flask import request, Blueprint
from flask_restx import fields, Api, Resource
from uuid import uuid4

from main import swagger
from rest import request_handle, Response, BaseResource

##################################################
# Demo route
##################################################
hello_ns = swagger.namespace('hello', description='APIs for simple testing')
swagger.add_namespace(hello_ns)

@hello_ns.route('/test-add')
class TestAdd(BaseResource):
    @hello_ns.doc('test a + b + c')
    @hello_ns.param('a', 'Argument a', type=int)
    @hello_ns.param('b', 'Argument b', type=int)
    @request_handle
    def get(self):
        a = int(request.args['a'])
        b = int(request.args['b'])
        sm = a + b

        resp = Response(data={})
        resp.data['a'] = a
        resp.data['b'] = b
        resp.data['sum'] = sm
        return resp
