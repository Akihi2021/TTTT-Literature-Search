from log import logger

from context import swagger, openAlex
from rest import request_handle, Response, BaseResource, fields, response_model
from flask import request

from route.user import success_response_model
from service.paper import do_comment, get_comment

paper_ns = swagger.namespace('paper', description='APIs for paper authors, papers')
swagger.add_namespace(paper_ns)

comment_parser = swagger.parser()
comment_parser.add_argument('user_id', type=int, required=True, help='ID of the user')
comment_parser.add_argument('paper_id', type=str, required=True, help='OpenAlex ID of the paper')
comment_parser.add_argument('content', type=str, required=True, help='Content of the comment')

comment_model = swagger.model("CommentModel", model={
    "user_id": fields.String,
    "paper_id": fields.String,
    "content": fields.String,
    "time": fields.DateTime()
})

paper_data_model = swagger.model("SearchPapersSuccessData", model={
    "group_by": fields.String,
    "meta": fields.String,
    "results": fields.String('详情请见https://docs.openalex.org/about-the-data/work'),
    "comments": fields.List(fields.Nested(comment_model))
})

get_paper_response_model = paper_ns.inherit("SearchPapersSuccessResponse", response_model, {
    "data": fields.Nested(paper_data_model)
})

@paper_ns.route('/')
class PaperRecommend(BaseResource):
    @paper_ns.doc('Get paper')
    @paper_ns.param(name="id", description="The OpenAlex ID for this paper ", type=int)
    @paper_ns.response(200, 'success', get_paper_response_model)
    @request_handle
    def get(self):
        id = str(int(request.args['id']))
        ret = openAlex.get_list_of_works(filters={
            'openalex_id': 'https://openalex.org/W' + id
        })
        paper = next(ret)

        comments = get_comment(id)
        paper['comments'] = comments

        resp = Response(
            data=paper
        )
        return resp


@paper_ns.route('/comment')
class Comment(BaseResource):
    @paper_ns.doc('Comment on papers')
    @paper_ns.expect(comment_parser)
    @paper_ns.response(200, 'success', success_response_model)
    @request_handle
    def post(self):
        args = comment_parser.parse_args()

        success = do_comment(
            args['user_id'],
            args['paper_id'],
            args['content']
        )

        resp = Response(
            data=dict(
                success=success
            )
        )

        return resp
