from log import logger

from context import swagger, openAlex
from rest import request_handle, Response, BaseResource
from flask import request

from route.user import success_response_model
from service.paper import comment

paper_ns = swagger.namespace('paper', description='APIs for paper authors, papers')
swagger.add_namespace(paper_ns)

comment_parser = swagger.parser()
comment_parser.add_argument('user_id', type=int, required=True, help='ID of the user')
comment_parser.add_argument('paper_id', type=str, required=True, help='OpenAlex ID of the paper')
comment_parser.add_argument('content', type=str, required=False, help='Content of the comment')


@paper_ns.route('/comment')
class Comment(BaseResource):
    @paper_ns.doc('Comment on papers')
    @paper_ns.expect(comment_parser)
    @paper_ns.response(200, 'success', success_response_model)
    @request_handle
    def post(self):
        args = comment_parser.parse_args()

        success = comment(
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
