from fastapi import FastAPI

from app.api.config.settings import ApiSettings
from app.api.routes import health, reports


def create_app():
    api = FastAPI(title=ApiSettings.app_name)
    api.include_router(health.router, prefix=ApiSettings.api_prefix)
    api.include_router(reports.router, prefix=ApiSettings.api_prefix)
    return api


app = create_app()
