import requests
from conf import settings


class BackupServiceClient:
    @staticmethod
    def trigger_backup(backup_name: str):
        response = requests.post(
            f"{settings.BACKUP_SERVICE_URL}/FileManager/backup/trigger/{backup_name}",
            timeout=3,
        )

        return response.json()

    @staticmethod
    def trigger_all_backups():
        response = requests.post(
            f"{settings.BACKUP_SERVICE_URL}/FileManager/backup/trigger_all", timeout=3
        )

        return response.json()

    @staticmethod
    def list_backups():
        response = requests.post(
            f"{settings.BACKUP_SERVICE_URL}/FileManager/backup/list", timeout=3
        )

        return response.json()
