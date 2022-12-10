from log import logger

from context import swagger, openAlex
from rest import request_handle, Response, BaseResource
from flask import request

from route.search import search_authors_success_response_model, search_papers_success_response_model

recommend_ns = swagger.namespace('recommend', description='APIs for Recommend authors, papers')
swagger.add_namespace(recommend_ns)


@recommend_ns.route('/papers')
class PaperRecommend(BaseResource):
    @recommend_ns.doc('Recommend papers')
    @recommend_ns.param(name="num", description="number of papers to be recommended",
                        type=int, required=False, default=1)
    @recommend_ns.response(200, 'success', search_papers_success_response_model)
    @request_handle
    def get(self):
        data = []
        for _ in range(int(request.args["num"])):
            data.append(openAlex.get_random_work())

        resp = Response(
            data=data
        )

        return resp


@recommend_ns.route('/authors')
class AuthorRecommend(BaseResource):
    @recommend_ns.doc('Recommend authors')
    @recommend_ns.param(name="num", description="number of authors to be recommended", type=int, required=False,
                        default=1)
    @recommend_ns.response(200, 'success', search_authors_success_response_model)
    @request_handle
    def get(self):
        data = []
        for _ in range(int(request.args["num"])):
            data.append(openAlex.get_random_author())

        resp = Response(
            data=data
        )

        return resp

@recommend_ns.route('/concepts')
class AuthorRecommend(BaseResource):
    @recommend_ns.doc('Recommend concepts')
    @recommend_ns.param(name="num", description="number of concepts to be recommended", type=int, required=False,
                        default=1)
    @recommend_ns.response(200, 'success', search_authors_success_response_model)
    @request_handle
    def get(self):
        data = []
        for _ in range(int(request.args["num"])):
            data.append(openAlex.get_random_concept())

        resp = Response(
            data=data
        )

        return resp
