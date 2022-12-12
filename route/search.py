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
    @search_ns.param(name="keyword", description="Keywords to search for papers", type=str, location="json")
    @search_ns.param(name="content", description="Search content(title|time|author|abstract|"")", type=str,
                     default="null", location="json")
    @search_ns.param(name="type", description="filter type(dissertation,book,journal 任选,用逗号隔开)", type=str,
                     default="null", location="json")
    @search_ns.param(name="institution", description="institution name", type=str, default="null", location="json")
    @search_ns.param(name="time", description="publication year", type=str, default="null", location="json")
    @search_ns.param(name="author", description="author name", type=str, default="null", location="json")
    @search_ns.param(name="page", description="Page number of search results", type=int, default=1, location="json")
    @search_ns.param(name="per_page", description="Number of works displayed per page", type=int, default=25,
                     location="json")
    @search_ns.response(200, 'success', search_papers_success_response_model)
    @request_handle
    def get(self):
        data = []
        filters = {}
        content = str(request.args["content"])
        type = str(request.args["type"])
        institution = str(request.args["institution"])
        time = str(request.args["time"])
        if time == 'null':
            time = ""
        else:
            filters = {
                'publication_year': time
            }
        author = str(request.args["author"])
        types = ''
        if type != "null":
            types1 = type.split(",")
            for i in range(0, len(types1) - 1):
                types = types + types1[i]
                types = types + "|"
            types = types.strip("|")
            filters = dict(filters, **{
                'type': types
            })
        institution_ids = ''
        if institution != "null":
            for i in openAlex.get_list_of_institutions(filters={'display_name.search': institution}, pages=[1]):
                id_0 = [ids.get('id') for ids in i.get('results')]
                for j in range(0, len(id_0) - 1):
                    institution_ids = institution_ids + id_0[j]
                    institution_ids = institution_ids + "|"
            institution_ids = institution_ids.strip("|")
            filters = dict(filters, **{
                'institution.id': institution_ids
            })
        author_ids = ''
        if author != "null":
            for i in openAlex.get_list_of_authors(filters={'display_name.search': author}, pages=[1]):
                id_0 = [ids.get('id') for ids in i.get('results')]
                for j in range(0, len(id_0) - 1):
                    author_ids = author_ids + id_0[j]
                    author_ids = author_ids + "|"
            author_ids = author_ids.strip("|")
            filters = dict(filters, **{
                'author.id': author_ids
            })
        if content == "null":
            for work in openAlex.get_list_of_works(search=str(request.args["keyword"]),
                                                   filters=filters,
                                                   pages=[int(request.args["page"])],
                                                   per_page=int(request.args["per_page"])):
                data.append(work)
        if content == 'title':
            for work in openAlex.get_list_of_works(
                    filters=dict({'title.search': str(request.args["keyword"])}, **filters),
                    pages=[int(request.args["page"])],
                    per_page=int(request.args["per_page"])):
                data.append(work)
        if content == 'abstract':
            for work in openAlex.get_list_of_works(
                    filters=dict({'abstract.search': str(request.args["keyword"])}, **filters),
                    pages=[int(request.args["page"])],
                    per_page=int(request.args["per_page"])):
                data.append(work)
        if content == 'time':
            for work in openAlex.get_list_of_works(
                    filters=dict({'publication_year': str(request.args["keyword"])}, **filters),
                    pages=[int(request.args["page"])],
                    per_page=int(request.args["per_page"])):
                data.append(work)
        if content == 'author':
            author_ids = ''
            if institution != "null":
                for i in openAlex.get_list_of_authors(filters={'display_name.search': str(request.args["keyword"])},
                                                      pages=[1]):
                    id_0 = [ids.get('id') for ids in i.get('results')]
                    for j in range(0, len(id_0) - 1):
                        author_ids = author_ids + id_0[j]
                        author_ids = author_ids + "|"
                author_ids = author_ids.strip("|")
            for work in openAlex.get_list_of_works(filters=dict({
                'author.id': author_ids}, **filters),
                    pages=[int(request.args["page"])],
                    per_page=int(request.args["per_page"])):
                data.append(work)

        resp = Response(
            data=data
        )
        return resp


@search_ns.route('/authors')
class PaperRecommend(BaseResource):
    @search_ns.doc('Get authors searched')
    @search_ns.param(name="keyword", description="Keywords to search for authors", type=str, location="json")
    @search_ns.param(name="page", description="Page number of search results", type=int, default=1, location="json")
    @search_ns.param(name="per_page", description="Number of authors displayed per page", type=int, default=25,
                     location="json")
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


@search_ns.route('/AdvancedSearch')
class PaperRecommend(BaseResource):
    @search_ns.doc('Get papers searched')
    @search_ns.param(name="title", description="search title", type=str, default='null', location="json")
    @search_ns.param(name="abstract", description="Search abstract", type=str, default="null", location="json")
    @search_ns.param(name="author", description="author name", type=str, default="null", location="json")
    @search_ns.param(name="type", description="filter type(dissertation,book,journal 任选,用逗号隔开)", type=str,
                     default="null", location="json")
    @search_ns.param(name="and1", description="title的and|not", type=str,
                     default="and", location="json")
    @search_ns.param(name="and2", description="abstract的and|not", type=str,
                     default="and", location="json")
    @search_ns.param(name="and3", description="author的and|not", type=str,
                     default="and", location="json")
    @search_ns.param(name="from", description="论文发表开始日期", type=str, default="null", location="json")
    @search_ns.param(name="to", description="论文发表结束日期", type=str, default="null", location="json")
    @search_ns.param(name="page", description="Page number of search results", type=int, default=1, location="json")
    @search_ns.param(name="per_page", description="Number of authors displayed per page", type=int, default=25,
                     location="json")
    @search_ns.response(200, 'success', search_papers_success_response_model)
    @request_handle
    def get(self):
        data = []
        type = str(request.args["type"])
        title = str(request.args["title"])
        author = str(request.args["author"])
        abstract = str(request.args["abstract"])
        from_date = str(request.args["from"])
        to_date = str(request.args["to"])
        and1 = str(request.args["and1"])
        and2 = str(request.args["and2"])
        and3 = str(request.args["and3"])
        author_ids = ''
        if author != "null":
            for i in openAlex.get_list_of_authors(filters={'display_name.search': author}, pages=[1]):
                id_0 = [ids.get('id') for ids in i.get('results')]
                for j in range(0, len(id_0) - 1):
                    author_ids = author_ids + id_0[j]
                    author_ids = author_ids + "|"
            author_ids = author_ids.strip("|")
        types = ''
        filters = {}
        if type != "null":
            types1 = type.split(",")
            for i in range(0, len(types1) - 1):
                types = types + types1[i]
                types = types + "|"
            types = types.strip("|")
            filters = dict(filters, **{
                'type': types
            })
        if title != 'null':
            if and1 == "not":
                filters = dict(filters, **{
                    'title': "!" + title
                })
            else:
                filters = dict(filters, **{
                    'title': title
                })
        if abstract != 'null':
            if and2 == "not":
                filters = dict(filters, **{
                    'abstract': "!" + abstract
                })
            else:
                filters = dict(filters, **{
                    'abstract': abstract
                })
        if author != 'null':
            if and3 == "not":
                filters = dict(filters, **{
                    'author.id': "!" + author_ids
                })
            else:
                filters = dict(filters, **{
                    'author.id': author_ids
                })
        if from_date != 'null':
            filters = dict(filters, **{
                'from_publication_date': from_date
            })
        if to_date != 'null':
            filters = dict(filters, **{
                'to_publication_date': to_date
            })
        for work in openAlex.get_list_of_works(filters=filters,
                                               pages=[int(request.args["page"])],
                                               per_page=int(request.args["per_page"])):
            data.append(work)

        resp = Response(
            data=data
        )
        return resp


@search_ns.route('/AuthorId')
class GetPaper(BaseResource):
    @search_ns.doc('Get paper by author id')
    @search_ns.param(name="id", description="The OpenAlex ID for this author ", type=int, location="json")
    @search_ns.param(name="page", description="Page number of search results", type=int, default=1, location="json")
    @search_ns.param(name="per_page", description="Number of authors displayed per page", type=int, default=25,
                     location="json")
    @search_ns.response(200, 'success', search_papers_success_response_model)
    @request_handle
    def get(self):
        data = []
        id = str(int(request.args['id']))
        for work in openAlex.get_list_of_works(filters={'author.id': 'https://openalex.org/A' + id},
                                               pages=[int(request.args["page"])],
                                               per_page=int(request.args["per_page"])):
            for result in work.get('results'):
                data.append({'title': result.get('title'), 'type': result.get('type')})

        resp = Response(
            data=data
        )
        return resp
