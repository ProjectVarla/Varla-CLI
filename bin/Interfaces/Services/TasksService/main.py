from os import getenv

import requests
from dotenv import load_dotenv
from fastapi import status
from requests import ConnectionError, ReadTimeout

from Models import FilterType, ListRenderType, Pair, Task, Todo
from Models.Exceptions import ServiceUnavailable
from VarlaLib import VarlaCLI as Varla
from VarlaLib.Shell.List.List_Control import Control
from VarlaLib.Shell.List.main import Schema, Table, render

load_dotenv()

HOST = getenv("TASKS_SERVICE_URL")


class TasksManager:

    long_listing: ListRenderType = ListRenderType.NORMAL
    filterType: FilterType = FilterType.NORMAL

    @staticmethod
    def delete_task(task_id: int):
        response = requests.delete(
            f"{HOST}/api/tasks/delete/task/{task_id}", timeout=3)
        if (response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE):
            raise ServiceUnavailable()

        return response.json()

    @staticmethod
    def delete_todo(todo_id: int):
        response = requests.delete(
            f"{HOST}/api/tasks/delete/todo/{todo_id}", timeout=3)
        if (response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE):
            raise ServiceUnavailable()

        return response.json()

    @staticmethod
    def create_task(task: Task.Base):
        response = requests.post(
            f"{HOST}/api/tasks/insert/task/", json=task.dict(), timeout=3)
        if (response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE):
            raise ServiceUnavailable()

        return response.json()

    @staticmethod
    def create_todo(task_id: int, todo: Todo.Base):
        response = requests.post(
            f"{HOST}/api/tasks/insert/todo/{task_id}", json=todo.dict(), timeout=3)
        if (response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE):
            raise ServiceUnavailable()

        return response.json()

    @staticmethod
    def modify_task(task_id: int, task: Task.Edit):
        response = requests.put(
            f"{HOST}/api/tasks/update/task/{task_id}", json=task.dict(), timeout=3)
        if (response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE):
            raise ServiceUnavailable()

        return response.json()

    @staticmethod
    def modify_todo(todo_id: int, todo: Todo.Edit):
        response = requests.put(
            f"{HOST}/api/tasks/update/todo/{todo_id}", json=todo.dict(), timeout=3)
        if (response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE):
            raise ServiceUnavailable()

        return response.json()

    @staticmethod
    def get_tasks(filter: Task.Filter):
        response = requests.post(
            f"{HOST}/api/tasks/get/tasks", data=filter.json(), timeout=3)
        if (response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE):
            raise ServiceUnavailable()

        return response.json()

    @staticmethod
    def get_todos(filter: Todo.Filter):
        response = requests.post(
            f"{HOST}/api/tasks/get/todos", data=filter.json(), timeout=3)
        return response.json()

    @staticmethod
    def get_id_from_cursor(items: list, cursor: Pair):
        return Task.Object(**items[cursor.x]).id

    @staticmethod
    def list_tasks(
            filter: Task.Filter = Task.Filter(),
    ):

        filter.is_archived = TasksManager.filterType == FilterType.ARCHIVED

        tasks = TasksManager.get_tasks(filter)

        columns = []
        if TasksManager.long_listing == ListRenderType.NORMAL:
            columns = [
                Schema(0, "id", "ID"),
                Schema(1, "title", "Title"),
                Schema(2, "description", "Description")
            ]

        TasksManager.list_test(
            items=tasks,
            columns=columns,
            on_enter=lambda cursor: (
                TasksManager.list_todos(
                    Todo.Filter(
                        task_id=TasksManager.get_id_from_cursor(
                            tasks, cursor
                        )))
            ),
            on_render=lambda cursor: render(
                Table(tasks, columns),
                cursor.x, cursor.y
            )
        )

    @staticmethod
    def list_todos(
        filter: Todo.Filter = Todo.Filter(),
    ):

        filter.is_archived = TasksManager.filterType == FilterType.ARCHIVED

        todos = TasksManager.get_todos(filter=filter)

        columns = []
        if TasksManager.long_listing == ListRenderType.NORMAL:
            columns = [
                Schema(0, "id", "ID"),
                Schema(1, "text", "Text"),
                Schema(2, "checked", "checked")
            ]

        TasksManager.list_test(
            items=todos,
            columns=columns,
            on_enter=lambda count: print(count),
            on_render=lambda cursor: render(
                Table(todos, columns), cursor.x, cursor.y
            )
        )

    @staticmethod
    def list_test(
            items, columns, on_enter, on_render,
    ):
        try:

            table: Table = Table(items)

            control = Control(
                dimension=table.dimension,
                on_enter=lambda count: on_enter(count),
                on_render=lambda cursor: on_render(cursor)
            )

            control.print()
            control.listen()

            Varla.clear()

        except ReadTimeout:
            return Varla.say("timeout")

        except ConnectionError:
            return Varla.say("Varla is Offline!")

        except ServiceUnavailable:
            return Varla.say("Tasks service is Offline!")

        except Exception as err:
            # raise err
            Varla.error(str(err))

    @staticmethod
    def controler(items, columns, on_enter, on_render):

        table: Table = Table(items)

        control = Control(
            dimension=table.dimension,
            on_enter=lambda count: on_enter(count),
            on_render=lambda cursor: on_render(cursor)
        )

        control.print()
        control.listen()
