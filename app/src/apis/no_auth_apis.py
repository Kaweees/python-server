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
            status,
        )
from fastapi.responses import JSONResponse

# ======================================================================================================================
# Custom module imports
# ======================================================================================================================
from app.src.schema import BaseItem

# ======================================================================================================================
# Logging configuration
# ======================================================================================================================
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# ======================================================================================================================
# Module level objects
# ======================================================================================================================
router = APIRouter(prefix="/unauthd", tags=["unauthenticated"])
MOCK_DB = [{"name": "item1"},
           {"name": "item2"},
           {"name": "item3"}]

# ======================================================================================================================
# Routes
# ======================================================================================================================


@router.get("/items", response_class=JSONResponse, status_code=status.HTTP_200_OK)
async def get_items_unauthed(request: Request):
    return MOCK_DB


@router.patch("/items/{name}", status_code=status.HTTP_200_OK)
async def patch_example(request: Request, name: str):
    MOCK_DB[name] = BaseItem(name)


@router.post("/items/{name}", status_code=status.HTTP_200_OK)
async def post_example(request: Request, name: str):
    MOCK_DB[name] = BaseItem(name)


@router.delete("/items/{name}", response_class=JSONResponse, status_code=status.HTTP_200_OK)
async def delete_example(request: Request, name: str):
    del MOCK_DB[name]
