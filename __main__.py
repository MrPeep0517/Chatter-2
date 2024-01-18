time_form = "%H:%M"
# main imports
try:
    from rich import print
    from sys import stdout
    import os
    import pickle
    import platform
    import datetime
    import inquirer
    from datetime import datetime
    import sys
except ModuleNotFoundError as e:
    print("Could not use",e,"please add to pip")
    exit()
try:
    os.mkdir("C:/Users/Ethan/chatter-2")
except FileExistsError:
    pass


# defining main functions
write = stdout.write
def up(amount):
    '''Moves the printing line up a specified amount.'''
    write(f"\u001b[{amount}A")
def right(amount):
    '''Moves the printing line right a specified amount.'''
    write(f"\u001b[{amount}C")
def down(amount):
    '''Moves the printing line down a specified amount.'''
    up(-amount)
def left(amount):
    '''Moves the printing line left a specified amount.'''
    right(-amount)
def save(data, filename):
    '''Saves a file.'''
    with open(filename,"wb") as file:
        pickle.dump(data,file)
def load(filename):
    '''Loads in a file.'''
    with open(filename,"rb") as file:
        return pickle.load(file)
def clear():
    '''Clears the every action the code took.'''
    if "Windows" in platform.platform():
        os.system("cls")
    else:
        os.system("clear")
def choose(item_name:str,message:str,items:list):
    '''Allows you to choose between a few messages with the arrow keys.'''

    questions = [
        inquirer.List(
            item_name,
            message=message,
            choices=items,
        ),
    ]
    username = inquirer.prompt(questions)
    return username[item_name] 

pass_attempts = 0
cmd_helps = {
    "time":"prints the time",
    "date":"prints the date",
    "python":"runs the python interprter",
    "echo":"prints what you put",
    "exit":"stops the program",
    "settime":"changes the time formating",
    "add_user":"creates a new user"
}

print("hi i am chatter-2 your chatbot!")


# loads the user names
try:
    names = load(f"{os.environ['USERPROFILE']}/chatter-2/names.pk")
except FileNotFoundError:
    names = {}
    

# gets user names
def user_name_getter(names: list[str]):
    '''Gets the username from the user to log into chatter-2.'''
    print("please enter your username")
    username = input(">").capitalize()
    if username in names.keys():
        print(f"Welcome {username}")
        while True:
            pass_attempts = 0
            if pass_attempts == 3:
                print("you entered the wrong password too many times")
                exit()
            print("please enter your password")
            password_attempt = input(">")
            password_length = len(password_attempt) + 1
            up(1)
            print("*" * password_length)
            if password_attempt == names[username]:
                break
            print("Wrong password please try again")
            pass_attempts += 1
    else:
        while True:
            print("do you already have a chatter-2 account [Y]es or [N]o")
            add_user = input(">").lower()
            if add_user == "y":
                user_name_getter()
            elif add_user == "n":
                break
            else:
                continue
        while True:
            print("Create your password")
            password_attempt1 = input(">")
            password_attempt1_length = len(password_attempt1)
            password_attempt1_length += 1
            up(1)
            print("*" * password_attempt1_length)
            print("Confirm your password")
            password_attempt2 = input(">")
            password_attempt2_length = len(password_attempt2)
            password_attempt2_length += 1
            up(1)
            print("*" * password_attempt2_length)
            if password_attempt1 == password_attempt2:
                print("New user added")
                names[username] = password_attempt1
                break
            else:
                print("[red]PasswordMatchError:\n   password_attempt1 ≠≠ password_attempt2\nplease re-enter password[red]")
    
user_name_getter(names)


# IDK
save(names,f"{os.environ['USERPROFILE']}/chatter-2/names.pk")


# main loop
while True:
    running = True
    date = datetime.now()
    cmd = input("$>")
    if cmd == "help":
        for x,y in zip(cmd_helps.keys(),cmd_helps.values()):
            print(x,y)
    elif cmd == "exit":
        break
    elif cmd == "python":
        import sys

        indents = ["def", "if", "while", "for"]
        oldCmds = []

        def isindent(text):
            for indent in indents:
                if text.startswith(indent):
                    return True
            return False

        def seplist(list: list[str], sep=" ") -> str:
            things = ""
            for item in list:
                if item != list[-1]:
                    things += (item + sep)
                else:
                    things += item
            return things

        def isvalidindent(text):
            try:
                exec(text + "\n    pass")
            except:
                return False
            else:
                return True

        def pythonterm():
            oldCmds = []
            while True:
                pythonCmd = input(">>> ")
                if pythonCmd == "exit()":
                    return 0
                try:
                    pythonOut = eval(pythonCmd)
                    if pythonOut != None:
                        print(pythonOut)
                except:
                    try:
                        if isindent(pythonCmd):
                            if not isvalidindent(pythonCmd):
                                print(
                                    f"SyntaxError: invalid syntax\n{pythonCmd} is not valid",
                                    file=sys.stderr)
                            else:
                                oldCmds.append(pythonCmd)
                                while True:
                                    if oldCmds[-1] == "" and pythonCmd == "":
                                        exec(seplist(oldCmds, "\n"))
                                        break
                                    print("...", end=" ")
                                    pythonCmd = input()
                                    oldCmds.append(pythonCmd)
                        else:
                            exec(pythonCmd)
                    except Exception as e:
                        print(
                            f"SyntaxError: invalid syntax\n{pythonCmd} is not valid",
                            file=sys.stderr)

        if __name__ == "__main__":
            pythonterm()
    elif cmd.startswith("echo"):
        print(cmd[5:])
    elif cmd == "time":
        print(date.strftime(f"[white]{time_form}[white]"))
    elif cmd.startswith("strftime "):
        print(date.strftime(cmd[9:]))
    elif cmd == "date":
        print(date.strftime("[white]%m:%d:%Y[white]"))
    elif cmd == "settime":
        messsage = choose("Times","What format do you want to see the time?",
                        ["12:59 pm","24:59"])
        if messsage == "12:59 pm":
            time_form = "%I:%M %p"
        elif messsage == "24:59":
            time_form = "%H:%M"
    elif cmd == "dir(echo)":
        print("type echo and after type what you would like to be echoed\nEx: echo hello\n$ hello")
    elif cmd == "dir(python)":
        print("type python adn you will be brought into the python shell/interpreter")
    elif cmd == "dir(date)":
        print("type date to print the current date")
    elif cmd == "dir(time)":
        print("type time to print the current time")
    elif cmd == "dir(exit)":
        print("type exit to exit the chatter-2 terminal")
    elif cmd == "add_user":
        while True:
            print("please enter your username")
            username2 = input(">")
            if username2 in names.keys():
                print("please enter your password")
                password = input(">")
                break
            else:
                print(f'[red]Error:\n    "{username2}"\nDataBaseError: "{username2}" is not in data base[red]')
                continue
        if password == names.get(username2):
            print("create the new username")
            new_username = input(">").capitalize()
            print("create the new password")
            new_password1 = input(">")
            up(1)
            new_password1_length = len(new_password1)
            new_password1_length += 1
            print("*" * new_password1_length)
            print("comfirm your new password")
            new_password2 = input(">")
            up(1)
            new_password2_length = len(new_password2)
            new_password2_length += 1
            print("*" * new_password2_length)
            if new_password1 == new_password2:
                try:
                    names[new_username] = new_password2
                    print("new user added")
                except:
                    print('[red]Error:[red]\n    249    [yellow]save([yellow][purple]{[purple][blue]new_username: new_password2[blue][purple]}[purple], [blue]f[blue]"[green]os[green].[blue]environ[[blue]"USERPROFILE"[blue]][blue][pink]}[pink]/chatter-2/names.pk"[yellow])[yellow]\n[red]SaveError: save cannot be executed[red]')
    else:
        print(f'[red]Error:\n   "{cmd}"\nUndefinedCommandError: "{cmd}" is not defined: type "help" for avalible commands[red]')           
