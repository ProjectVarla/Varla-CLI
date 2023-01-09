import requests
from conf import settings
from VarlaLib.Shell import VarlaCLI as Varla


class BackupServiceClient:
    @staticmethod
    def trigger_backup(backup_name: str):
        try:
            response = requests.post(
                f"{settings.BACKUP_SERVICE_URL}/FileManager/backup/trigger/{backup_name}",
                timeout=3,
            )
            return response.json()
        except Exception as e:
            Varla.error(e)

    @staticmethod
    def trigger_all_backups():
        try:
            response = requests.post(
                f"{settings.BACKUP_SERVICE_URL}/FileManager/backup/trigger_all",
                timeout=3,
            )
            return response.json()
        except Exception as e:
            Varla.error(e)

    @staticmethod
    def list_backups():
        try:
            response = requests.post(
                f"{settings.BACKUP_SERVICE_URL}/FileManager/backup/list", timeout=3
            )
            return response.json()
        except Exception as e:
            Varla.error(e)
