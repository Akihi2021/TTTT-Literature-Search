import string

from flask import request
from flask_restx import fields

from log import logger

from context import swagger, openAlex
from rest import request_handle, Response, BaseResource, response_model

search_ns = swagger.namespace('search', description='APIs for Search')
swagger.add_namespace(search_ns)

search_papers_success_data_model = swagger.model("SearchPapersSuccessData", model={
    "group_by": fields.String,
    "meta": fields.String,
    "results": fields.List(fields.String('详情请见https://docs.openalex.org/about-the-data/work'))
})

search_papers_success_response_model = search_ns.inherit("SearchPapersSuccessResponse", response_model, {
    "data": fields.Nested(search_papers_success_data_model)
})
search_authors_success_data_model = swagger.model("SearchAuthorsSuccessData", model={
    "group_by": fields.String,
    "meta": fields.String,
    "results": fields.List(fields.String('详情请见https://docs.openalex.org/about-the-data/author'))
})

search_authors_success_response_model = search_ns.inherit("SearchAuthorsSuccessResponse", response_model, {
    "data": fields.Nested(search_authors_success_data_model)
})


####################################################################################################
# Search API with OpenAlex
# TODO: Implement Search Related APIs with call to OpenAlex here
#       1. Search Paper with keyword
#       2. Search Author with keyword
#       3. Filter Paper with keyword
#       4. Filter Author with keyword
#       5. Whatever required by front-end developer requires.
# NOTE: 1. Refer to `route.recommend` For usage of OpenAlex Python Client
# LINK:
#       1. https://docs.openalex.org/api/get-lists-of-entities/filter-entity-lists
#       2. https://docs.openalex.org/api/get-lists-of-entities/search-entity-lists
####################################################################################################

@search_ns.route('/papers')
class PaperRecommend(BaseResource):
    @search_ns.doc('Get papers searched')
    @search_ns.param(name="keyword", description="Keywords to search for papers", type=str)
    @search_ns.param(name="page", description="Page number of search results", type=int, default=1)
    @search_ns.param(name="per_page", description="Number of works displayed per page", type=int, default=25)
    @search_ns.response(200, 'success', search_papers_success_response_model)
    @request_handle
    def get(self):
        data = []
        for work in openAlex.get_list_of_works(search=str(request.args["keyword"]), pages=[int(request.args["page"])],
                                               per_page=int(request.args["per_page"])):
            data.append(work)

        resp = Response(
            data=data
        )
        return resp


@search_ns.route('/authors')
class PaperRecommend(BaseResource):
    @search_ns.doc('Get authors searched')
    @search_ns.param(name="keyword", description="Keywords to search for authors", type=str)
    @search_ns.param(name="page", description="Page number of search results", type=int, default=1)
    @search_ns.param(name="per_page", description="Number of authors displayed per page", type=int, default=25)
    @search_ns.response(200, 'success', search_authors_success_response_model)
    @request_handle
    def get(self):
        data = []
        for author in openAlex.get_list_of_authors(search=str(request.args["keyword"]),
                                                   pages=[int(request.args["page"])],
                                                   per_page=int(request.args["per_page"])):
            data.append(author)

        resp = Response(
            data=data
        )
        return resp

