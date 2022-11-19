from typing import Optional

import typer

from Models import FilterType, ListRenderType, Task, TasksTypes, Todo

from .main import TasksManager as TM

tasks = typer.Typer(add_completion=True)

delete = typer.Typer(add_completion=True)
create = typer.Typer(add_completion=True)
update = typer.Typer(add_completion=True)
retrieve = typer.Typer(add_completion=True)


tasks.add_typer(delete, name="delete")
tasks.add_typer(create, name="create")
tasks.add_typer(update, name="update")
tasks.add_typer(retrieve, name="retrieve")


@tasks.command("list", help="[Optional] Shows all Tasks in an interactive way.")
@tasks.callback(invoke_without_command=True)
def list_tasks(
    ctx: typer.Context,
    show_archived: bool = typer.Option(False, "--show-archived", "-a"),
    show_all: bool = typer.Option(False, "--show-all", "-A"),
    long_listing: bool = typer.Option(False, "--long-listing", "-l")
):

    if long_listing:
        TM.long_listing = ListRenderType.LONG_LISTING

    if show_archived:
        TM.filterType = FilterType.ARCHIVED

    if show_all:
        print("Show all not implemented yet!")
        # TM.filterType = FilterType.ALL

    print("hello?", long_listing)
    if ctx.invoked_subcommand is not None:
        return

    TM.list_tasks()


@create.command("task")
def create_task(
    title: str,
    description: str = typer.Option("", "--description", "-d"),
    color: str = typer.Option("", "--color", "-c"),
    archived: bool = typer.Option(False, "--archived", "-a")

):
    TM.create_task(
        Task.Base(
            title=title,
            description=description,
            color=color,
            archived=archived
        )
    )


@create.command("todo")
def create_todo(
    task_id: int,
    text: str,
    archived: bool = typer.Option(False, "--archived", "-a"),
    pinned: bool = typer.Option(False, "--pinned", "-p")
):
    TM.create_todo(
        task_id=task_id,
        todo=Todo.Base(
            text=text,
            archived=archived,
            pinned=pinned,
            checked=False
        )
    )


@update.command("task")
def modify_task(
    task_id: int,
    title: str = typer.Option(None, "--title", "-t"),
    description: str = typer.Option(None, "--description", "-d"),
    color: str = typer.Option(None, "--color", "-c"),
    archived: Optional[bool] = typer.Option(
        None, "--archive/--un-archive", "-a/-una"),

):
    print(task_id, title, description, color, archived)
    TM.modify_task(
        task_id=task_id,
        task=Task.Edit(
            title=title,
            description=description,
            color=color,
            archived=archived
        )
    )


@update.command("todo")
def modify_todo(
    todo_id: int,
    text: str = typer.Option(None, "--text", "-t"),
    archived: bool = typer.Option(None, "--archived", "-a"),
    pinned: bool = typer.Option(None, "--pinned", "-p")
):
    TM.modify_todo(
        todo_id=todo_id,
        todo=Todo.Edit(
            text=text,
            archived=archived,
            pinned=pinned,
            checked=False
        )
    )


@delete.command("task")
def delete_task(id: int):
    typer.confirm(
        f"Are you sure you want to delete task with id = {id}?",
        abort=True
    )

    TM.delete_task(id)

    print(TasksTypes.TASK, id, delete)


@delete.command("todo")
def delete_todo(id: int):
    typer.confirm(
        f"Are you sure you want to delete todo with id = {id}?",
        abort=True
    )

    TM.delete_todo(id)


@retrieve.command("task")
def retrieve_task(id: int):
    TM.list_tasks(filter=Task.Filter(id=id))


@retrieve.command("todo")
def retrieve_todo(id: int, in_task: bool = typer.Option(False, "--in-task", "-t")):
    filter = Todo.Filter()

    if in_task:
        filter.task_id = id
    else:
        filter.id = id

    TM.list_todos(filter)
