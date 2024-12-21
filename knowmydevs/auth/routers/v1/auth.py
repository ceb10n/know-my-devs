from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.security import HTTPBasic

from knowmydevs.auth.payloads import TokenCredential, TokenForm
from knowmydevs.auth.responses import TokenResponse
from knowmydevs.auth.services import auth_service

router = APIRouter(prefix="/oauth2", tags=["Authentication"])


@router.post("/token", status_code=200)
async def login(
    form: Annotated[TokenForm, Form()],
    credentials: Annotated[TokenCredential, Depends(HTTPBasic())],
) -> TokenResponse:
    return await auth_service.issue_token(credentials, form)
