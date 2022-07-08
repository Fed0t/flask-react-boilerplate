import json
from .request import ModexRequest


class PermissionManagement:

    def set_personal_data_access(self, entity_name, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            '/core/v1/api/security/_Permissions/Group/' + entity_name, params)

