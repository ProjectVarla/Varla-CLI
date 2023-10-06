import json
from asyncio import (
    FIRST_COMPLETED,
    AbstractEventLoop,
    Future,
    Queue,
    create_task,
    new_event_loop,
    wait,
)
from sys import stdout
from threading import Thread
from typing import Any, Set

from Interfaces.Cores import Notifications
from VarlaLib.Context import context
from VarlaLib.Shell import VarlaCLI as Varla
from websockets.exceptions import ConnectionClosed
from websockets.frames import Close
from websockets.legacy.client import connect


def exit_from_event_loop_thread(
    loop: AbstractEventLoop,
    stop: Future[None],
) -> None:
    loop.stop()
    stop.done()
    context.thread = None


def print_during_input(string: str) -> None:
    stdout.write(
        # Save cursor position
        "\N{ESC}7"
        # Add a new line
        "\N{LINE FEED}"
        # Move cursor up
        "\N{ESC}[A"
        # Insert blank line, scroll last line down
        "\N{ESC}[L"
        # Print string in the inserted blank line
        f"{string}\N{LINE FEED}"
        # Restore cursor position
        "\N{ESC}8"
        # Move cursor down
        "\N{ESC}[B"
    )
    stdout.flush()


def print_over_input(string: str) -> None:
    stdout.write(
        # Move cursor to beginning of line
        "\N{CARRIAGE RETURN}"
        # Delete current line
        "\N{ESC}[K"
        # Print string
        f"{string}\N{LINE FEED}"
    )
    stdout.flush()


async def nothing():
    return None


async def run_client(
    uri: str,
    loop: AbstractEventLoop,
    inputs: Queue[str],
    stop: Future[None],
) -> None:
    try:
        websocket = await connect(uri)
    except Exception as exc:
        Varla.error(f"Failed to connect to {uri}: {exc}.")
        exit_from_event_loop_thread(loop, stop)
        # return

    try:
        while True:
            incoming: Future[Any] = create_task(websocket.recv())
            outgoing: Future[Any] = create_task(inputs.get())
            done: Set[Future[Any]]
            pending: Set[Future[Any]]
            done, pending = await wait(
                [incoming, outgoing, stop], return_when=FIRST_COMPLETED
            )

            # Cancel pending tasks to avoid leaking them.
            if incoming in pending:
                incoming.cancel()
            if outgoing in pending:
                outgoing.cancel()

            if incoming in done:
                try:
                    message = incoming.result()
                except ConnectionClosed:
                    break
                else:
                    message = json.loads(message)

                    if not context.socket_id:
                        context.socket_id = message["connection_id"]

                    Varla.say(
                        message["text"],
                        name=message["from"] if "from" in message.keys() else "Varla",
                    )

            if outgoing in done:

                message = outgoing.result()
                # await websocket.send(message)
                Varla.parse_command(message)

            if stop in done:
                break

        # await Varla.say(e)
    finally:
        # if websocket:
        await websocket.close()
        assert websocket.close_code is not None and websocket.close_reason is not None
        close_status = Close(websocket.close_code, websocket.close_reason)
        # if not OK send in error
        Varla.say(f"Connection closed: {close_status}.")
        # Varla.say(str(websocket))
        exit_from_event_loop_thread(loop, stop)


class NotificationIntegration:
    @classmethod
    def parse(cls, commands):

        commands.append("")
        if commands[0] == "disconnect":
            cls.stop()

        elif commands[0] in ["connect", "reconnect"]:
            if commands[1] in ["-n", "--new"]:
                cls.clear_id()

            cls.connect()

        elif commands[0] == "close":
            cls.close()

        elif commands[0] == "id":
            if commands[1] in ["-c", "--clear"]:
                cls.clear_id()
            else:
                cls.get_id()

        elif commands[0] == "list":
            cls.list_subscribtions()
            pass
        elif commands[0] == "sub":
            cls.subscribe(commands[1:-1])
        elif commands[0] == "unsub":
            cls.unsubscribe(commands[1:-1])

        else:
            Varla.say("commands cannot be empty!")

    @classmethod
    def stop(
        cls,
    ):
        if not context.thread:
            Varla.say("Nothing to stop")
            return
        context.loop.call_soon_threadsafe(context.stop.set_result, None)

        # Wait for the eventevent loop to terminate.
        context.thread.should_abort_immediately = True

        try:
            context.thread.join()
            context.loop.close()
        except Exception as e:
            print(e)
            pass  # runtime error cannot join thread for some reason

        context.thread = None
        Varla.say("Closed")

    @classmethod
    def connect(cls):

        if context.socket_id:
            uri = f"ws://localhost:8500/reconnect/{context.socket_id}"
        else:
            uri = "ws://localhost:8500/connect"

        if context.thread:
            Varla.say("Already connected to socket!")
            return
        context.loop = new_event_loop()

        async def queue_factory() -> Queue[str]:
            return Queue()

        context.inputs: Queue[str] = context.loop.run_until_complete(queue_factory())

        context.stop: Future[None] = context.loop.create_future()

        context.loop.create_task(
            run_client(uri, context.loop, context.inputs, context.stop)
        )

        context.thread = Thread(target=context.loop.run_forever)
        context.thread.start()

    @classmethod
    def get_id(cls):
        print(context.socket_id)

    @classmethod
    def clear_id(cls):
        context.socket_id = None

    @classmethod
    def disconnect(cls):
        Notifications.disconnect()

    @classmethod
    def close(cls):
        Notifications.close()
        # cls.clear_id()

    @classmethod
    def subscribe(cls, channels: str):
        if not channels:
            raise ValueError("Expecting Channels")
        Notifications.subscribe(channels)

    @classmethod
    def unsubscribe(cls, channel_names: str):
        if not channel_names:
            raise ValueError("Expecting channel_names")
        Notifications.unsubscribe(channel_names)

    @classmethod
    def list_subscribtions(
        cls,
    ):
        Varla.say(Notifications.list_subscribtions())
