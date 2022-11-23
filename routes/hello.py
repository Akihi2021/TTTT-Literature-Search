from flask import request
from log import logger

from main import app, api
from rest import request_handle, Response, BaseResource

##################################################
# Demo route
##################################################
hello_ns = api.namespace('hello', description='APIs for simple testing')
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


##################################################
# Demo route with URL query
##################################################
paper_ns = api.namespace(
    'recomendation', description='Online Recommendation Scenarios')


@paper_ns.route('/user/<string:user_id>/papers')
class VideoRecommend(BaseResource):
    @paper_ns.doc('Get all paper of certain user')
    @request_handle
    def get(self, user_id):
        logger.info('接收到用户"{}"的论文请求'.format(user_id))
        return


@paper_ns.route('/user/<string: user_id>/category/<string:category_id>/paper')
class CategoryVideoRecommend(BaseResource):
    @paper_ns.doc('')
    @request_handle
    def get(self, user_id, category_id):
        logger.info('接收到用户"{}"、论文类别"{}"的论文请求'.format(user_id, category_id))
        return
