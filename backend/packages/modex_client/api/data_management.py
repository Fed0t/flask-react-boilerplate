import json
from .request import ModexRequest


class DataManagement:
    def insert_record(self, entity_name, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            "/core/v1/api/data/" + entity_name, params, node_type="auth"
        )

    def view_record(self, entity_name, record_id, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.get_request(
            "/core/v1/api/data/" + entity_name + "/" + record_id, params
        )

    def get_all_records(self, entity_name, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.get_request("/core/v1/api/data/" + entity_name, params)

    def list_records(self, entity_name, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            "/core/v1/api/data/" + entity_name + "/list", params, node_type="auth"
        )

    def count_records(self, entity_name, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            "/core/v1/api/data/" + entity_name + "/list", params, node_type="auth"
        )

    def count_records(self, entity_name, record_id, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            "/core/v1/api/data/" + entity_name + "/" + record_id,
            params,
            node_type="auth",
        )

    def update_records(self, entity_name, record_id, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.patch_request(
            "/core/v1/api/data/" + entity_name + "/" + record_id,
            params,
            node_type="auth",
        )

    def replace_records(self, entity_name, record_id, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.put_request(
            "/core/v1/api/data/" + entity_name + "/" + record_id,
            params,
            node_type="auth",
        )

    def delete_record(self, entity_name, record_id, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.put_request(
            "/core/v1/api/data/" + entity_name + "/" + record_id,
            params,
            node_type="auth",
        )
