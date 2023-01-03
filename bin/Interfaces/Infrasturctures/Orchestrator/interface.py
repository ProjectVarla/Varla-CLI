import typer

from .main import OrchestratorInfrastructureClient as OIC


orchestrator = typer.Typer(add_completion=True)


@orchestrator.command("up")
def orchestrator_up(service_name: str):
    print(OIC.up(service_name))


@orchestrator.command("down")
def orchestrator_down(service_name: str):
    print(OIC.down(service_name))


@orchestrator.command("restart")
def orchestrator_restart(service_name: str):
    print(OIC.restart(service_name))


@orchestrator.command("status")
def orchestrator_status(service_name: str):
    print(OIC.status(service_name))
