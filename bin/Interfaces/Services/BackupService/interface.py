import typer
from .main import BackupServiceClient


backup = typer.Typer(add_completion=True)


@backup.command("trigger")
def trigger_backup_all(
    title: str = typer.Argument(
        "", help="Name of the backup or write 'ALL' to run all backups"
    )
):
    if title == "ALL":
        print(BackupServiceClient.trigger_all_backup())
    else:
        print(BackupServiceClient.trigger_backup(title))
