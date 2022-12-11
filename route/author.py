import string

from flask import request
from flask_restx import fields

from log import logger

from context import swagger, openAlex
from rest import request_handle, Response, BaseResource, response_model

author_ns = swagger.namespace('author', description='Author related API')
swagger.add_namespace(author_ns)


get_author_data_model = swagger.model("GetAuthorData", model={
    "group_by": fields.String,
    "meta": fields.String,
    "results": fields.List(fields.String('详情请见https://docs.openalex.org/about-the-data/author'))
})

get_author_response_model = author_ns.inherit("GetAuthorResponse", response_model, {
    "data": fields.Nested(get_author_data_model)
})


@author_ns.route('/')
class PaperRecommend(BaseResource):
    @author_ns.doc('Get author with author OpenAlex Id')
    @author_ns.param(name="id", description="The OpenAlex ID for this author ", type=int)
    @author_ns.response(200, 'success', get_author_response_model)
    @request_handle
    def get(self):
        ret = openAlex.get_list_of_authors(filters={
            'openalex_id': 'https://openalex.org/A' + str(int(request.args['id']))
        })
        author = next(ret)

        resp = Response(
            data=author
        )

        return resp


