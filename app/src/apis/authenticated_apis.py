# ======================================================================================================================
# Author: Sam Dunham (sdunham@nvidia.com)
# ======================================================================================================================

# ======================================================================================================================
# Built-in modules
# ======================================================================================================================
import sys
import logging

# ======================================================================================================================
# Third party modules
# ======================================================================================================================
from fastapi import (
            APIRouter,
            Request,
            Security,
            status,
        )

from fastapi.responses import JSONResponse

# ======================================================================================================================
# Custom module imports
# ======================================================================================================================
import app.src.schema as schema
from app.src.config import auth_settings

# ======================================================================================================================
# Logging configuration
# ======================================================================================================================
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# ======================================================================================================================
# Module level objects
# ======================================================================================================================
router = APIRouter(prefix="/authd", tags=["authenticated"])
MOCK_DB = [{"name": "item1", "cheap": True},
           {"name": "item2", "cheap": False},
           {"name": "item3", "cheap": True}]


# ======================================================================================================================
# Routes
# ======================================================================================================================


@router.get("/expnsive_items",
            dependencies=[Security(auth_settings.azure_scheme)],
            response_class=JSONResponse,
            status_code=status.HTTP_200_OK)
async def get_items_authenticated(request: Request):
    return [schema.ExpensiveItem(name=item['name']) for item in MOCK_DB if not item['cheap']]


@router.patch("/items/{name}",
              dependencies=[Security(auth_settings.azure_scheme)],
              status_code=status.HTTP_200_OK)
async def patch_example_authenticated(request: Request, name: str):
    MOCK_DB[name] = schema.CheapItem(name)
    MOCK_DB[name] = schema.ExpensiveItem(name)


@router.post("/items/{name}",
             dependencies=[Security(auth_settings.azure_scheme)],
             status_code=status.HTTP_200_OK)
async def post_example_authenticated(request: Request, name: str):
    MOCK_DB[name] = schema.CheapItem(name)
    MOCK_DB[name] = schema.ExpensiveItem(name)


@router.delete("/items/{name}",
               dependencies=[Security(auth_settings.azure_scheme)],
               response_class=JSONResponse,
               status_code=status.HTTP_200_OK)
async def delete_example_authenticated(request: Request, name: str):
    del MOCK_DB[name]
