from typing import List

import typer
from Models import ServicesFilter

from .main import OrchestratorInfrastructureClient as OIC

orchestrator = typer.Typer(add_completion=True)


@orchestrator.command("up")
def orchestrator_up(
    services_names: List[str],
):
    for status in OIC.up(
        ServicesFilter(
            services_names=services_names,
            select_all=services_names[0].lower() == "all",
        )
    ):
        print(status)


@orchestrator.command("down")
def orchestrator_down(
    services_names: List[str],
):
    for status in OIC.down(
        ServicesFilter(
            services_names=services_names,
            select_all=services_names[0].lower() == "all",
        )
    ):
        print(status)


@orchestrator.command("restart")
def orchestrator_restart(
    services_names: List[str],
):
    for status in OIC.restart(
        ServicesFilter(
            services_names=services_names,
            select_all=services_names[0].lower() == "all",
        )
    ):
        print(status)


@orchestrator.command("status")
def orchestrator_status(
    services_names: List[str],
):
    for status in OIC.status(
        ServicesFilter(
            services_names=services_names,
            select_all=services_names[0].lower() == "all",
        )
    ):
        print(status)


@orchestrator.command("list")
def orchestrator_list():
    for service_name in OIC.list():
        print(service_name)
