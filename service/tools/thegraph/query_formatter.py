from service.tools.thegraph.queries import Queries


class QueryFormatter:
    """
    This class is the GQL query formatter for the Falcon API
    It is used to format the queries found in the 'LendingQueries' and 'TellerQueries' files
    """

    def __init__(self):
        self.gql_queries = {
            "current_price_usd": Queries.QUERY__CURRENT_PRICE,
        }

    def format_query(self, query: str, address: str):
        return query.format(address=address)
