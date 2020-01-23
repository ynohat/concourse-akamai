import requests
from akamai import edgegrid
from requests import Session


class EdgeGridSession(requests.Session):
    def __init__(self, host, client_token, client_secret, access_token,
                 headers_to_sign=None, max_body=131072):
        super().__init__()
        self.host = host
        self.auth = edgegrid.EdgeGridAuth(
            access_token=access_token,
            client_token=client_token,
            client_secret=client_secret
        )

    def request(self, method, url, *args, **kwargs):
        url = "https://{host}{url}".format(host=self.host, url=url)
        return super().request(method, url, *args, **kwargs)
