# ======================================================================================================================
# Author: Sam Dunham (sdunham@nvidia.com)
# ======================================================================================================================

# ======================================================================================================================
# Built-in modules
# ======================================================================================================================
import os
from unittest import unittest

# ======================================================================================================================
# Third-party modules
# ======================================================================================================================
from fastapi import APIRouter

# ======================================================================================================================
# Custom modules
# ======================================================================================================================
from app.src.config import AuthSettings
from app.src.webapp import (
    create_app,
    configure_middleware,
    add_routers,
    initialize_web_app,
    )


# ======================================================================================================================
# Test Cases
# ======================================================================================================================
def initialize_web_app(routers: List[APIRouter], settings: Union[BaseSettings, None] = None) -> FastAPI:



class TestWebApp(unittest.TestCase):
    def setUp(self):
        os.environ["APP_CLIENT_ID"] = "TEST_APP_CLIENT_ID"
        os.environ["TENANT_ID"] = "TEST_TENANT_ID"
        os.environ["OPENAPI_CLIENT_ID"] = "TEST_OPENAPI_CLIENT_ID"
        os.environ["API_SCOPE"] = "TEST_API_SCOPE"
        os.environ["REDIRECT_URL"] = "TEST_REDIRECT_URL"

    def test_app_no_auth_creation(self):
        app = create_app()
        assert app

    def test_app_with_auth(self):
        settings = AuthSettings()
        app = create_app(settings)
        assert app

    def test_configure_middleware(self):
        app = create_app()
        self.assertIsNone(configure_middleware(app))

    def test_add_routers(self):
        app = create_app()
        routers = [APIRouter()]*3
        self.assertIsNone(add_routers(app, routers))


