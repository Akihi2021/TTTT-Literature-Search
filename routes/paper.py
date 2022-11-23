from flask import request
from log import logger

from main import app, swagger
from rest import request_handle, Response, BaseResource

# ##################################################
# # Demo route with URL query
# ##################################################
paper_ns = swagger.namespace('paper', description='Online Recommendation Scenarios')
swagger.add_namespace(paper_ns)


@paper_ns.route('/user/<string:user_id>/papers')
class VideoRecommend(BaseResource):
    @paper_ns.doc('Get all paper of certain user')
    @request_handle
    def get(self, user_id):
        logger.info('接收到用户"{}"的论文请求'.format(user_id))
        return


@paper_ns.route('/user/<string: user_id>/category/<string:category_id>/papers')
class CategoryVideoRecommend(BaseResource):
    @paper_ns.doc('')
    @request_handle
    def get(self, user_id, category_id):
        logger.info('接收到用户"{}"、论文类别"{}"的论文请求'.format(user_id, category_id))
        return
