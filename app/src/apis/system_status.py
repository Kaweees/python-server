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

# ======================================================================================================================
# Custom module imports
# ======================================================================================================================
from app.src.config import auth_settings

# ======================================================================================================================
# Logging configuration
# ======================================================================================================================
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# ======================================================================================================================
# Module level objects
# ======================================================================================================================
router = APIRouter(prefix="/health")

# ======================================================================================================================
# Routes
# ======================================================================================================================


@router.get("/alive",  status_code=status.HTTP_200_OK)
async def liveness_check(request: Request):
    return {"alive": "OK"}
