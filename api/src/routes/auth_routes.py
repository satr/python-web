from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
import os

oauth = OAuth()
oauth.register(
    name="oidc",
    server_metadata_url=os.getenv("OIDC_DISCOVERY_URL"),  # e.g. https://dev-xxx.auth0.com/.well-known/openid-configuration
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),              # for public SPA you’d use PKCE; for server use secret
    client_kwargs={"scope": "openid profile email"},
)

def get_auth_router() -> APIRouter:
    router = APIRouter(prefix="", tags=["auth"])

    @router.get("/login")
    async def login(request: Request):
        redirect_uri = request.url_for("auth_callback")
        return await oauth.oidc.authorize_redirect(request, redirect_uri)

    @router.get("/auth/callback")
    async def auth_callback(request: Request):
        token = await oauth.oidc.authorize_access_token(request)  # exchanges code → tokens (handles PKCE)
        userinfo = token.get("userinfo") or await oauth.oidc.userinfo(token=token)
        request.session["user"] = dict(userinfo)
        request.session["access_token"] = token["access_token"]
        return RedirectResponse(url="/me")

    @router.get("/me")
    def me(request: Request):
        user = request.session.get("user")
        if not user:
            raise HTTPException(401, "Not logged in")
        return user

    return router
