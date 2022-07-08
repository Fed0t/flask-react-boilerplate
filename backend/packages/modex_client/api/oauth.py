import json
from .request import ModexRequest
import os
import urllib
from packages.modex_client.utils import save_config_file

class Authorization():

    def __init__(self):
        self.config = {
            "CLIENT_ID": os.getenv("CLIENT_ID"),
            "CLIENT_SECRET": os.getenv("CLIENT_SECRET"),
            "REDIRECT_URI": os.getenv("REDIRECT_URI"),
        }

    def authorize(self) -> json:
        data_params = urllib.parse.urlencode({
                "response_type": "code",
                "client_id": self.config["CLIENT_ID"],
                "redirect_uri": self.config['CLIENT_SECRET'],
        })
        modex_request = ModexRequest()
        token = modex_request.get_request("/oauth/authorize?" + data_params)
        print(token)
        save_config_file(str(token))
        return token

    def generate_token(self, params) -> json:
        data_params = params.copy()
        data_params.update(
            {
                "client_id": self.config["CLIENT_ID"],
                "client_secret": self.config["CLIENT_SECRET"],
                "response_type": "code",
                "grant_type": "exchange_token",
            }
        )
        modex_request = ModexRequest()
        token = modex_request.post_request("/oauth/token", data_params)
        # print(token)
        save_config_file(str(token))
        return token