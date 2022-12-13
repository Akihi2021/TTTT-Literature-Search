import string

from flask import request
from flask_restx import fields


from context import swagger, openAlex
from rest import request_handle, Response, BaseResource, response_model
from service import author


author_ns = swagger.namespace('author', description='API for Author')
swagger.add_namespace(author_ns)


author_data_model = swagger.model("AuthorData", model={
    "group_by": fields.String,
    "meta": fields.String,
    "results": fields.List(fields.String('详情请见https://docs.openalex.org/about-the-data/author'))
})

author_response_model = author_ns.inherit("AuthorResponse", response_model, {
    "data": fields.Nested(author_data_model)
})

author_paper_data_model = swagger.model("AuthorPapersData", model={
    "title": fields.String,
    "type": fields.String
})

author_papers_reponse_model = author_ns.inherit("AuthorPapersResponse", response_model, {
    "data": fields.List(fields.Nested(author_paper_data_model))
})

related_author_data = swagger.model("RelatedAuthor", model={
    "name": fields.String
})

related_author_response_model = author_ns.inherit("RelatedAuthorResponse", response_model, {
    "data": fields.List(fields.Nested(related_author_data))
})


@author_ns.route('/')
class PaperRecommend(BaseResource):
    @author_ns.doc('Get author with author OpenAlex Id')
    @author_ns.param(name="id", description="The OpenAlex ID for this author ", type=int)
    @author_ns.response(200, 'success', author_response_model)
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


@author_ns.route('/papers')
class GetPaper(BaseResource):
    @author_ns.doc('Get ')
    @author_ns.param(name="id", description="The OpenAlex ID for this author ", type=int)
    @author_ns.response(200, 'success', author_papers_reponse_model)
    @request_handle
    def get(self):
        author_id = str(int(request.args.get("id")))

        data = author.get_title_and_type_of_papers(author_id)

        resp = Response(
            data=data
        )

        return resp


@author_ns.route('/related_authors')
class GetRelatedAuthor(BaseResource):
    @author_ns.doc('Get ')
    @author_ns.param(name="id", description="The OpenAlex ID for this author", type=int)
    @author_ns.response(200, 'success', related_author_response_model)
    @request_handle
    def get(self):
        id = str(int(request.args.get("id")))

        data = author.get_related_authors(id)

        resp = Response(
            data=data
        )

        return resp





