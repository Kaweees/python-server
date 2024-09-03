# ======================================================================================================================
# Author: Sam Dunham (sdunham@nvidia.com)
# ======================================================================================================================

# ======================================================================================================================
# Built-in modules
# ======================================================================================================================
import os
from unittest import unittest

# ======================================================================================================================
# Custom modules
# ======================================================================================================================
from app.src.config import Settings, AuthSettings

# ======================================================================================================================
# Test Cases
# ======================================================================================================================


class TestSettingsBasic(unittest.TestCase):

    def test_base_settings(self):
        settings = Settings()
        self.assertIsNotNone(settings)

    def test_auth_settings(self):
        settings = AuthSettings()
        self.assertIsNone(settings.APP_CLIENT_ID)
        self.assertIsNone(settings.TENANT_ID)
        self.assertIsNone(settings.OPENAPI_CLIENT_ID)
        self.assertIsNone(settings.API_SCOPE)
        self.assertIsNone(settings.REDIRECT_URL)
        self.assertEquals(settings.REDIRECT_URL, "/oauth2-redirect")


class TestSettingsAuthenticated(unittest.TestCase):
    def setUp(self):
        os.environ["APP_CLIENT_ID"] = "TEST_APP_CLIENT_ID"
        os.environ["TENANT_ID"] = "TEST_TENANT_ID"
        os.environ["OPENAPI_CLIENT_ID"] = "TEST_OPENAPI_CLIENT_ID"
        os.environ["API_SCOPE"] = "TEST_API_SCOPE"
        os.environ["REDIRECT_URL"] = "TEST_REDIRECT_URL"

    def test_auth_settings(self):
        settings = AuthSettings()
        self.assertEquals(settings.APP_CLIENT_ID, "TEST_APP_CLIENT_ID")
        self.assertEquals(settings.TENANT_ID, "TEST_TENANT_ID")
        self.assertEquals(settings.OPENAPI_CLIENT_ID, "TEST_OPENAPI_CLIENT_ID")
        self.assertEquals(settings.API_SCOPE, "TEST_API_SCOPE")
        self.assertEquals(settings.REDIRECT_URL, "TEST_REDIRECT_URL")
