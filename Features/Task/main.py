from utility.Context import context
import requests
from os import getenv

from dotenv import load_dotenv
from pynput import keyboard
from VarlaLib import clear

load_dotenv()

HOST = getenv("HOST")

tasks_cursor = 1
todos_cursor = 1
selected_task = 0
ctrl = False
tasks = []
todos = []

def tasks_manager():

    global tasks
    tasks = get_tasks()

    render_tasks(tasks)

    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    clear()
    pass

def get_tasks():
    response = requests.post(f"{HOST}/api/tasks/get/tasks",data="{}")
    return response.json()

def get_todos(task_id:int):
    response = requests.post(f"{HOST}/api/tasks/get/todos",data='{"task_id": '+str(task_id)+'}')
    return response.json()
    

def render_tasks(tasks):
    clear()
    global tasks_cursor
    for idx,task in enumerate(tasks,start=1):
        print(f"{'#' if idx == tasks_cursor and not selected_task else ' ':>4}",idx,task["title"])
        if selected_task == idx:
            for idx,todo in enumerate(todos,start=1):
                print(f"{'#' if idx == todos_cursor else ' ':>6} [{'X' if todo['checked'] else ' '}]",idx,todo["text"])
    pass


def go_up():
    global tasks_cursor
    global todos_cursor
    global selected_task

    if selected_task:
        if todos_cursor > 1 : todos_cursor-=1
    else:
        if tasks_cursor > 1 : tasks_cursor-=1

def go_down():
    global tasks_cursor
    global todos_cursor

    if selected_task:
        if todos_cursor < len(todos): todos_cursor+=1    
    else:
        if tasks_cursor < len(tasks): tasks_cursor+=1    


def select_task():
    global selected_task
    global tasks_cursor
    global todos

    selected_task = tasks_cursor
    todos = get_todos(tasks[selected_task-1]["id"])

def unselect_task():
    global selected_task
    global todos
    global todos_cursor

    selected_task = 0
    todos_cursor = 1
    todos = []


def on_press(key):
    global tasks_cursor
    global ctrl
    global tasks

    try:
        if key == keyboard.Key.ctrl:    ctrl = True
        if key == keyboard.Key.up:      go_up()
        if key == keyboard.Key.down:    go_down()
        if key == keyboard.Key.right:   select_task()
        if key == keyboard.Key.left:    unselect_task()


        render_tasks(tasks)
        if ctrl and key.char == ('c'):  return False

    except AttributeError: pass

def on_release(key):
    global ctrl

    if key == keyboard.Key.esc: return False
    if key == keyboard.Key.ctrl: ctrl = False

    try: 
        if ctrl and key.char == ('c'): return False
    except AttributeError: pass

 