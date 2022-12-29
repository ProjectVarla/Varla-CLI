from os import getenv

import requests
from dotenv import load_dotenv


load_dotenv()

HOST = getenv("BACKUP_SERVICE_URL")


class BackupServiceClient:
    @staticmethod
    def trigger_backup(backup_name: str):
        response = requests.post(
            f"{HOST}/FileManager/backup/trigger/{backup_name}", timeout=3
        )

        return response.json()

    @staticmethod
    def trigger_all_backup():
        response = requests.post(f"{HOST}/FileManager/backup/trigger_all", timeout=3)

        return response.json()
