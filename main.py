from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
from pydantic.v1 import BaseSettings
from pydantic import AnyHttpUrl, computed_field
from fastapi_azure_auth import MultiTenantAzureAuthorizationCodeBearer
from router.admin_router import admin_router


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS = ['http://localhost:8000']
    OPENAPI_CLIENT_ID: str = "7a240826-ab39-41f3-ad74-3c603c57ded2"
    APP_CLIENT_ID: str = "e0c093cd-70ac-43cd-b558-6b3398871bed"
    TENANT_ID: str = "84c31ca0-ac3b-4eae-ad11-519d80233e6f"
    SCOPE_DESCRIPTION: str = "user_impersonation"


    @property
    def SCOPES(self) -> dict:
        return {
            'api://e0c093cd-70ac-43cd-b558-6b3398871bed/user_impersonation': 'user_impersonation',
        }


settings = Settings()

app = FastAPI(
    swagger_ui_oauth2_redirect_url=f'/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': "7a240826-ab39-41f3-ad74-3c603c57ded2",
    },
)

# CORS middleware to allow all origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
#
# # azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
# #     app_client_id=settings.APP_CLIENT_ID,
# #     tenant_id=settings.TENANT_ID,
# #     scopes=settings.SCOPES,
# # )
#
azure_scheme = MultiTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.APP_CLIENT_ID,
    scopes={
        f'api://{settings.APP_CLIENT_ID}/user_impersonation': 'user_impersonation',
    },
    validate_iss=False
)

@app.on_event('startup')
async def load_config() -> None:
    """
    Load OpenID config on startup.
    """
    await azure_scheme.openid_config.load_config()

@app.get("/welcome", dependencies=[Security(azure_scheme)])
async def welcome():
    """
    welcome screen
    """
    return {"message": "Welcome to Flight Reservation System"}


app.include_router(admin_router, prefix="/api/v1", tags=["admin"], dependencies=[Security(azure_scheme)])
# app.include_router(flight_router, prefix="/api/v1", tags=["flight"], dependencies=[Security(azure_scheme)])
# app.include_router(user_router, prefix="/api/v1", tags=["user"], dependencies=[Security(azure_scheme)])
