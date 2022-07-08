import json
from .request import ModexRequest


class UserManagement:

    def create_user(self, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            '/core/v1/api/system/createUser',
            params, node_type="auth")

    def update_user(self, user_id, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            '/core/v1/api/system/updateUserProfile/' + user_id,
            params, node_type="auth")

    def add_user_to_group(self, group_id, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            '/core/v1/api/system/updateUserProfile/' + group_id,
            params, node_type="auth")

    def remove_user_from_group(self, group_id, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            '/core/v1/api/system/removeUserFromGroup/' + group_id,
            params, node_type="auth")

    def get_current_user_profile(self, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            '/core/v1/api/system/userProfile/',
            params, node_type="auth")

    def get_user_profile_by_username_or_id(self, usernameOrId, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            '/core/v1/api/system/getUser/'+usernameOrId,
            params, node_type="auth")

    def change_password(self, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            '/core/v1/api/system/changePassword',
            params, node_type="auth")

    def update_password(self, params) -> json:
        modex_request = ModexRequest(authenticated=True)
        params = json.dumps(params)
        return modex_request.post_request(
            '/core/v1/api/system/updatePassword',
            params, node_type="auth")