from keboola.http_client import HttpClient
from requests.exceptions import HTTPError

BASE_URL = "https://api.ehub.cz/v3/"

PUBLIC_ENDPOINT = "public"

CAMPAIGN_LIST_ENDPOINT = "campaigns"

DEFAULT_PAGE_SIZE = 50


class EHubClientException(Exception):
    pass


class EHubClient(HttpClient):
    def __init__(self):
        super().__init__(BASE_URL)

    def get_public_campaigns(self):
        endpoint_path = f"{PUBLIC_ENDPOINT}/{CAMPAIGN_LIST_ENDPOINT}"
        parameters = {"perPage": DEFAULT_PAGE_SIZE, "page": 1}
        return self._paginate_endpoint(endpoint_path, parameters)

    def _paginate_endpoint(self, endpoint, parameters):
        has_more = True
        while has_more:
            response = self._get_endpoint(endpoint, parameters)
            yield response.get("campaigns")
            if response.get("totalItems") <= parameters.get("page") * 50:
                has_more = False
            parameters["page"] += 1

    def _get_endpoint(self, endpoint, parameters):
        try:
            return self.get(endpoint_path=endpoint, params=parameters)
        except HTTPError as http_err:
            raise EHubClientException(http_err) from http_err
