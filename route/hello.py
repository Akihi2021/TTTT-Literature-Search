##################################################
# Demo route for POST AND GET METHODS
##################################################

from flask import request, Blueprint
from context import swagger
from rest import request_handle, Response, BaseResource

hello_ns = swagger.namespace('hello', description='APIs for simple testing')
swagger.add_namespace(hello_ns)

parser = swagger.parser()
parser.add_argument('a', location='json', type=int, required=True, help="operand a")
parser.add_argument('b', location='json', type=int, required=True, help='operand b')


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

    @hello_ns.doc('test a + b with post')
    @hello_ns.expect(parser)
    @request_handle
    def post(self):
        args = parser.parse_args()
        resp = Response(data={})
        resp.data["ans"] = args["a"] + args["b"]
        return resp