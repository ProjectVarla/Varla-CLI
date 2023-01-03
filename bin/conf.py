from typing import Optional
from pydantic import BaseSettings, validator
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):

    DEBUG_MODE: Optional[bool] = False

    APP_NAME: str = "Varla-CLI"
    APP_TYPE: str = "Interface"

    GATEWAY_URL: str

    NOTIFICATION_CORE_URL: Optional[str]
    BACKUP_SERVICE_URL: Optional[str]
    TASKS_SERVICE_URL: Optional[str]

    DEFAULT_CHANNEL: Optional[str]

    @validator("NOTIFICATION_CORE_URL", always=True)
    def notification_core_url_validator(cls, v, values):
        return v if v else values["GATEWAY_URL"]

    @validator("BACKUP_SERVICE_URL", always=True)
    def backup_service_url_validator(cls, v, values):
        return v if v else values["GATEWAY_URL"]

    @validator("TASKS_SERVICE_URL", always=True)
    def tasks_service_url_validator(cls, v, values):
        return v if v else values["GATEWAY_URL"]


settings = Settings()
