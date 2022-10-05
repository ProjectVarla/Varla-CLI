import readline
def say(message:str):
    print(f"\033[36m\033[01mVarla >> \033[0m{message}")

def ask(message:str=""):
    if message: message = f"\033[36mVarla >> \033[0m{message}\n"
    try:
        return input(message+"\033[33m\033m  #   >>\033[0m ")
    except KeyboardInterrupt:
        print()
        say("Goodbye Boss!")
        exit()

def heartbeat():
    say("Connecting to main-frame...")
    say("Connected!")

def history():
    for i in range(readline.get_current_history_length()):
        print(i,readline.get_history_item(i))