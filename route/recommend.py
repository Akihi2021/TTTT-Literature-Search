from flask import request
from random_words import RandomWords

from context import swagger, openAlex
from rest import request_handle, Response, BaseResource
from route.search import search_authors_success_response_model, search_papers_success_response_model

recommend_ns = swagger.namespace('recommend', description='APIs for Recommend Authors, Papers, Concepts')
swagger.add_namespace(recommend_ns)

word_generator = RandomWords()


@recommend_ns.route('/papers')
class PaperRecommend(BaseResource):
    @recommend_ns.doc('Recommend papers')
    @recommend_ns.param(name="num", description="number of papers to be recommended",
                        type=int, required=False, default=1)
    @recommend_ns.response(200, 'success', search_papers_success_response_model)
    @request_handle
    def get(self):
        num = int(request.args["num"])
        data = []
        while len(data) < num:
            papers = next(openAlex.get_list_of_works(
                filters={
                    'display_name.search': word_generator.random_word()
                },
                pages=[1],
                per_page=num))
            data.extend(papers.get("results"))

        resp = Response(
            data=data[:num]
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
        num = int(request.args["num"])
        data = []

        while len(data) < num:
            authors = next(openAlex.get_list_of_works(
                filters={
                    'display_name.search': word_generator.random_word()
                },
                pages=[1],
                per_page=num))
            data.extend(authors.get("results"))

        resp = Response(
            data=data[:num]
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
        num = int(request.args["num"])
        data = []

        while len(data) < num:
            concepts = next(openAlex.get_list_of_works(
                filters={
                    'display_name.search': word_generator.random_word()
                },
                pages=[1],
                per_page=num))
            data.extend(concepts.get("results"))

        resp = Response(
            data=data[:num]
        )

        return resp


if __name__ == "__main__":
    num = 10
    concepts = next(openAlex.get_list_of_concepts(
        filters={
            'display_name.search': word_generator.random_word()
        },
        pages=[1],
        per_page=num))

    resp = Response(
        data=concepts
    )

    print(len(concepts.get("results")))
