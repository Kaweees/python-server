# ======================================================================================================================
# Author: Sam Dunham (sdunham@nvidia.com)
# ======================================================================================================================

# ======================================================================================================================
# Built-in imports
# ======================================================================================================================
import os
import logging
from typing import Union

# ======================================================================================================================
# Third-party imports
# ======================================================================================================================
from pydantic import computed_field
from pydantic_settings import BaseSettings
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
from dotenv import load_dotenv


# ======================================================================================================================
# Logging configuration
# ======================================================================================================================
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


# ======================================================================================================================
# Environment setup
# ======================================================================================================================
load_dotenv()

# ======================================================================================================================
# classes
# ======================================================================================================================


class Settings(BaseSettings):
    class Config:
        env_file = ".env"


class AuthSettings(BaseSettings):
    APP_CLIENT_ID: Union[str, None] = os.getenv("APP_CLIENT_ID")
    TENANT_ID: Union[str, None] = os.getenv("TENANT_ID")
    OPENAPI_CLIENT_ID: Union[str, None] = os.getenv("OPENAPI_CLIENT_ID")
    API_SCOPE: Union[str, None] = os.getenv("API_SCOPE")
    REDIRECT_URL: str = os.getenv("REDIRECT_URL", "/oauth2-redirect")
    azure_scheme: SingleTenantAzureAuthorizationCodeBearer = (
        SingleTenantAzureAuthorizationCodeBearer(
            app_client_id=APP_CLIENT_ID,
            tenant_id=TENANT_ID,
            scopes={
                f"api://{APP_CLIENT_ID}/{API_SCOPE}": API_SCOPE,
            },
        )
    )

    @computed_field
    @property
    def SWAGGER_UI_INIT_OATH(self) -> dict:
        return {
            "usePkceWithAuthorizationCodeGrant": True,
            "clientId": self.OPENAPI_CLIENT_ID,
            "scopes": self.API_SCOPE,
        }

    @computed_field
    @property
    def OPENAPI_AUTHORIZATION_URL(self) -> str:
        return f"https://login.microsoftonline.com/{self.TENANT_ID}/oauth2/v2.0/authorize"

    @computed_field
    @property
    def OPENAPI_TOKEN_URL(self) -> str:
        return f"https://login.microsoftonline.com/{self.TENANT_ID}/oauth2/v2.0/token"

    @computed_field
    @property
    def AZURE_BACKEND_API_APP_REGISTRATION_URL(self) -> str:
        return f"https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Overview/appId/{self.APP_CLIENT_ID}"

    @computed_field
    @property
    def AZURE_FRONTEND_API_APP_REGISTRATION_URL(self) -> str:
        return f"https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Overview/appId/{self.OPENAPI_CLIENT_ID}"

# ======================================================================================================================
# Module level constants
# ======================================================================================================================


auth_settings = AuthSettings()
