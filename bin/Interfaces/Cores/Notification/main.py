import asyncio
import os
import signal
import sys
import threading
from typing import Any, Set

import requests
from conf import settings
from Models.Cores import NotificationMessage
from VarlaLib.Context import context
from VarlaLib.Decorations import Colorize, Colors
from VarlaLib.Shell import VarlaCLI as Varla

from websockets.exceptions import ConnectionClosed
from websockets.frames import Close
from websockets.legacy.client import connect


class Notifications:
    @staticmethod
    def push(message: NotificationMessage):
        try:
            response = requests.get(
                f"{settings.GATEWAY_URL}/push/{message.channel_name}/{message.message}",
                timeout=3,
            )
            return response.json()
        except Exception as e:
            Varla.error(e)

    @staticmethod
    def bind(channel_name: str, host: str = ""):

        host = host if host else settings.NOTIFICATION_CORE_URL
        Varla.clear(top_text=host.upper(), bottom_text=channel_name)

        try:
            test(f"ws://{host}/bind/{channel_name}")
            # ws = create_connection(f"ws://{host}/connect")
            # while True:
            #     print_during_input("< " + ws.recv())
            #     # Varla.say(ws.recv(), name=channel_name)

        except KeyboardInterrupt:
            # ws.close()
            Varla.clear()

        except Exception as e:
            Varla.clear()
            Varla.error(e)

    @staticmethod
    def list_subscribtions():

        try:
            response = requests.post(
                f"{settings.GATEWAY_URL}/list_subscribtions",
                json={
                    "connection_id": context.socket_id,
                },
                timeout=3,
            )
            return response.json()

        except Exception as e:
            Varla.error(e)

    @staticmethod
    def subscribe(channels: list[str]):
        print(channels)
        try:
            response = requests.post(
                # f"{settings.GATEWAY_URL}/subscribe",
                f"http://localhost:8500/subscribe",
                json={
                    "connection_id": context.socket_id,
                    "channels": [{"name": str(value)} for value in channels],
                },
                timeout=3,
            )
            return response.json()

        except Exception as e:
            Varla.error(e)

    @staticmethod
    def unsubscribe(channel_names: list[str]):

        try:
            response = requests.post(
                f"{settings.GATEWAY_URL}/unsubscribe",
                json={
                    "connection_id": context.socket_id,
                    "channel_names": channel_names,
                },
                timeout=3,
            )
            return response.json()

        except Exception as e:
            Varla.error(e)

    @staticmethod
    def disconnect():
        try:
            response = requests.post(
                f"{settings.GATEWAY_URL}/disconnect",
                json={"connection_id": context.socket_id},
                timeout=3,
            )
            return response.json()

        except Exception as e:
            Varla.error(e)

    @staticmethod
    def close():
        try:
            response = requests.post(
                f"{settings.GATEWAY_URL}/close",
                json={"connection_id": context.socket_id},
                timeout=3,
            )
            return response.json()

        except Exception as e:
            Varla.error(e)


def exit_from_event_loop_thread(
    loop: asyncio.AbstractEventLoop,
    stop: asyncio.Future[None],
) -> None:
    loop.stop()
    if not stop.done():
        # When exiting the thread that runs the event loop, raise
        # KeyboardInterrupt in the main thread to exit the program.
        if sys.platform == "win32":
            ctrl_c = signal.CTRL_C_EVENT
        else:
            ctrl_c = signal.SIGINT
        os.kill(os.getpid(), ctrl_c)


def print_during_input(string: str) -> None:
    sys.stdout.write(
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
    sys.stdout.flush()


def print_over_input(string: str) -> None:
    sys.stdout.write(
        # Move cursor to beginning of line
        "\N{CARRIAGE RETURN}"
        # Delete current line
        "\N{ESC}[K"
        # Print string
        f"{string}\N{LINE FEED}"
    )
    sys.stdout.flush()


async def run_client(
    uri: str,
    loop: asyncio.AbstractEventLoop,
    inputs: asyncio.Queue[str],
    stop: asyncio.Future[None],
) -> None:
    try:
        websocket = await connect(uri)
    except Exception as exc:
        print_over_input(f"Failed to connect to {uri}: {exc}.")
        exit_from_event_loop_thread(loop, stop)
        return
    else:
        print_during_input(f"Connected to {uri}.")

    try:
        while True:
            incoming: asyncio.Future[Any] = asyncio.create_task(websocket.recv())
            outgoing: asyncio.Future[Any] = asyncio.create_task(inputs.get())
            done: Set[asyncio.Future[Any]]
            pending: Set[asyncio.Future[Any]]
            done, pending = await asyncio.wait(
                [incoming, outgoing, stop], return_when=asyncio.FIRST_COMPLETED
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
                    if isinstance(message, str):
                        print_during_input(
                            Colorize(
                                text=f"FileManager >> ",
                                style=Colors.MD.BOLD,
                                foreground=Colors.FG.CYAN,
                            )
                            + message
                        )
                        # Varla.say(message, name=channel_name)

                    else:
                        print_during_input("< (binary) " + message.hex())

            if outgoing in done:
                message = outgoing.result()
                await websocket.send(message)

            if stop in done:
                break

    finally:
        await websocket.close()
        assert websocket.close_code is not None and websocket.close_reason is not None
        close_status = Close(websocket.close_code, websocket.close_reason)

        print_over_input(f"Connection closed: {close_status}.")

        exit_from_event_loop_thread(loop, stop)


def test(uri) -> None:

    try:
        import readline  # noqa
    except ImportError:  # Windows has no `readline` normally
        pass

    # Create an event loop that will run in a background thread.
    loop = asyncio.new_event_loop()

    # Due to zealous removal of the loop parameter in the Queue constructor,
    # we need a factory coroutine to run in the freshly created event loop.
    async def queue_factory() -> asyncio.Queue[str]:
        return asyncio.Queue()

    # Create a queue of user inputs. There's no need to limit its size.
    inputs: asyncio.Queue[str] = loop.run_until_complete(queue_factory())

    # Create a stop condition when receiving SIGINT or SIGTERM.
    stop: asyncio.Future[None] = loop.create_future()

    # Schedule the task that will manage the connection.
    loop.create_task(run_client(uri, loop, inputs, stop))

    # Start the event loop in a background thread.
    thread = threading.Thread(target=loop.run_forever)
    thread.start()

    # Read from stdin in the main thread in order to receive signals.
    try:
        while True:
            # Since there's no size limit, put_nowait is identical to put.
            message = Varla.ask()
            loop.call_soon_threadsafe(inputs.put_nowait, message)
    except (KeyboardInterrupt, EOFError):  # ^C, ^D
        loop.call_soon_threadsafe(stop.set_result, None)

    # Wait for the event loop to terminate.
    thread.join()

    # For reasons unclear, even though the loop is closed in the thread,
    # it still thinks it's running here.
    loop.close()
