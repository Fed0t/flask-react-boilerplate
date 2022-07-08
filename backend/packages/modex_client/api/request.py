import os
from requests_toolbelt import sessions
from requests.exceptions import ConnectionError, Timeout, RequestException, HTTPError, RetryError
import json
from packages.modex_client.utils import get_config_file

class ModexRequest:
    session = None
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys_config = get_config_file()
    config = {
        "URI": os.getenv("MODEX_URI"),
        "DATA_PORTS": os.getenv("MODEX_DATA_PORTS"),
        "AUTH_PORTS": os.getenv("MODEX_AUTH_PORTS"),
        "TOKEN": os.getenv("MODEX_TOKEN"),
    }
    def buildSession(self):
        http_ = sessions.BaseUrlSession(base_url=self.config['URI'])
        self.session = http_

    def __init__(self, authenticated=False):
        self.buildSession()
        if authenticated is True and self.sys_config is not None:
            self.session.headers.update(
                {"Authorization": "Bearer " + self.config["TOKEN"]}
            )

    def set_node_port(self, node_type):
        node_port = self.config['DATA_PORTS']
        if node_type == "auth":
            node_port = self.config['AUTH_PORTS']
        return node_port
       
    def build_endpoint(self, node_type):
        return ":" + str(self.set_node_port(node_type)) + "/services"

    def get_request(self, endpoint, node_type="data"):
        try:
            response = self.session.get(self.build_endpoint(node_type) + endpoint)
            jsonResponse = json.loads(response.text)
            return jsonResponse
        except (HTTPError, ConnectionError, Timeout, RequestException, RetryError) as errh:
            print(errh)
       

    def post_request(self, endpoint, params, node_type="data"):
        data_params = params
        node_port = self.set_node_port(node_type)

        self.session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"}
        )
        if node_type == "auth":
            self.session.headers.update({"Content-Type": "application/json"})

        try:
            response = self.session.post(
                self.build_endpoint(node_type) +  endpoint,
                data=data_params,
                json=data_params,
            )
            jsonResponse = json.loads(response.text)
            return jsonResponse
        except (HTTPError, ConnectionError, Timeout, RequestException, RetryError) as error_handler:
            raise error_handler

    def patch_request(self, endpoint, params, node_type="data"):
        data_params = params
        self.session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"}
        )

        if node_type == "auth":
            self.session.headers.update({"Content-Type": "application/json"})

        try:
            response = self.session.patch(
                self.build_endpoint(node_type) +  endpoint,
                data=data_params,
                json=data_params,
            )
            jsonResponse = json.loads(response.text)
            return jsonResponse
        except (HTTPError, ConnectionError, Timeout, RequestException, RetryError) as error_handler:
            raise error_handler

    def put_request(self, endpoint, params, node_type="data"):
        data_params = params
        self.session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"}
        )
        if node_type == "auth":
            self.session.headers.update({"Content-Type": "application/json"})

        try:
            response = self.session.put(self.build_endpoint(node_type) + endpoint,
                data=data_params,
                json=data_params,
                )
            jsonResponse = json.loads(response.text)
            return jsonResponse
        except (HTTPError, ConnectionError, Timeout, RequestException, RetryError) as error_handler:
            raise error_handler
