import requests
from django.contrib.auth import get_user_model
from octo.utils.generate import generate_code
from octo.logging import Logger, sanitize_message
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

User = get_user_model()


class OAuthHandler:
    EMAIL_FIELD = "email"
    NAME_FIELD = "name"

    def __init__(self, access_token) -> None:
        self.logger = Logger("oauth").get()
        self.access_token = access_token
        self.service_url = self.get_service_url()
        self.token_list = {"jwt": self.generate_jwt_token, "token": self.generate_token}

    def get_service_url(self) -> str:
        ""
        pass

    def validate_access_token(self) -> bool:
        ""
        pass

    def _get_headers(self):
        return {"Authorization": "Bearer " + {self.access_token}}

    def _fetch_data(self) -> dict | None:
        try:
            response = requests.get(self.service_url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            self.logger.error(sanitize_message("Failed to fetch user info: " + str(e)))
        return None

    def _get_user(self):
        user_info = self._fetch_data()

        if not user_info:
            return None

        email = str(user_info.get(self.EMAIL_FIELD, ""))
        username = str(email.split("@")[0] + "_" + generate_code(4))
        name = str(user_info.get(self.NAME_FIELD, username))

        return self.get_user(
            {
                "email": email,
                "username": username,
                "name": name,
            }
        )

    def get_user(self, data_user: dict):
        try:
            user, _ = User.objects.get_or_create(**data_user)
            return user
        except Exception as e:
            self.logger.error(
                sanitize_message("Error creating or retrieving user:" + str(e))
            )
            return None

    def validate_token(self, token_type):
        if token_type not in self.token_list:
            raise ValueError(
                f"Invalid token_type. Allowed values are: {list(self.token_list.keys())}"
            )

    def _generate(self, token_type: str):
        self.validate_token(token_type)
        if self.validate_access_token():
            user = self._get_user()
            if user:
                token_list = self.token_list.get(token_type)
                return token_list(user)
        return None

    def generate_jwt_token(self, user) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def generate_token(self, user) -> dict:
        token, _ = Token.objects.get_or_create(user=user)
        return token

    def generate(self, token_type: str):
        return self._generate(token_type)
