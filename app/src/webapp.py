# ======================================================================================================================
# Author: Sam Dunham (sdunham@nvidia.com)
# ======================================================================================================================

# ======================================================================================================================
# Built-in imports
# ======================================================================================================================
import os
import sys
import logging
from typing import List, Union
from contextlib import asynccontextmanager

# ======================================================================================================================
# Third-party imports
# ======================================================================================================================
from pydantic_settings import BaseSettings
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# ======================================================================================================================
# Logging configuration
# ======================================================================================================================
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# ======================================================================================================================
# Module constants and environment
# ======================================================================================================================
FRONTEND = os.getenv("CORS_URL", "http://localhost:3000")

# ======================================================================================================================
# functions
# ======================================================================================================================


def create_app(auth_settings: Union[BaseSettings, None] = None) -> FastAPI:
    if auth_settings:
        LOGGER.info("Creating fully authenticated application.")
        # FastAPI docs recommend using the "lifespan" function to define startup and shutdown processes.
        @asynccontextmanager
        async def app_lifecycle_mgmt(app: FastAPI):
            await auth_settings.azure_scheme.openid_config.load_config()
            yield

        app = FastAPI(
                lifespan=app_lifecycle_mgmt,
                swagger_ui_oath2_redirect_url=auth_settings.REDIRECT_URL,
                swagger_ui_init_oath=auth_settings.SWAGGER_UI_INIT_OATH,
                )
    else:
        LOGGER.info("Creating un-authenticated application.")
        app = FastAPI()

    return app


def configure_middleware(app: FastAPI) -> None:
    app.add_middleware(
            CORSMiddleware,
            allow_origins=[FRONTEND, "http://localhost:3000", "http://localhost:3001"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )


def add_routers(app: FastAPI, routers: List[APIRouter]) -> None:
    for router in routers:
        app.include_router(router)


def initialize_web_app(routers: List[APIRouter], settings: Union[BaseSettings, None] = None) -> FastAPI:
    app = create_app(settings)
    configure_middleware(app)
    add_routers(app, routers)
    return app
