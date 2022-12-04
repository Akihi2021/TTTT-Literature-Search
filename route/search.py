from log import logger

from context import swagger, openAlex
from rest import request_handle, Response, BaseResource

search_ns = swagger.namespace('search', description='APIs for search authors, papers')
swagger.add_namespace(search_ns)

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


if __name__ == "__main__":
    print(openAlex.get_random_work())