from octo.handler.oauth import OAuthHandler
import requests
from django.conf import settings


class OAuthGoogle(OAuthHandler):
    def get_service_url(self):
        return "https://www.googleapis.com/oauth2/v3/userinfo"

    def validate_access_token(self) -> bool:
        validation_url = "https://www.googleapis.com/oauth2/v3/tokeninfo"

        response = requests.get(
            validation_url, params={"access_token": self.access_token}
        )

        if response.status_code == 200:
            token_info = response.json()
            client_ids = settings.OCTO_OAUTH.get("google")

            if token_info["aud"] in client_ids:
                return True

        return False
