try:
    time_form = "%H:%M"
    
    try:
        from rich import print
        from sys import stdout
        import os
        import pickle
        import platform
        import datetime
        import inquirer
        from datetime import datetime
    except ModuleNotFoundError as e:
        print("Could not use",e,"please add to pip")
        exit()
    try:
        os.mkdir(f"{os.environ['USERPROFILE']}/chatter")
    except FileExistsError:
        pass
    
    write = stdout.write
    def up(amount):
        write(f"\u001b[{amount}A")
    def right(amount):
        write(f"\u001b[{amount}C")
    def down(amount):
        up(-amount)
    def left(amount):
        right(-amount)
    def save(data, filename):
        with open(filename,"wb") as file:
            pickle.dump(data,file)
    def load(filename):
        with open(filename,"rb") as file:
            return pickle.load(file)
    def clear():
        if "Windows" in platform.platform():
            os.system("cls")
        else:
            os.system("clear")
    def choose(item_name:str,message:str,items:list):

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
        "settime":"changes the time formating"
    }

    print("Hi I am chatter your chatbot!")

    def user_name_getter():
        try:
            names = load(f"{os.environ['USERPROFILE']}/chatter/names.pk")
        except FileNotFoundError:
            names = {}
            
        print("Please enter your username")
        username = input(">").lower()
        if username in names.keys():
            print(f"Welcome {username}")
            while True:
                pass_attempts = 0
                if pass_attempts == 3:
                    print("You entered the wrong password too many times")
                    exit()
                print("Please enter your password")
                password_attempt = input(">")
                password_length = len(password_attempt)
                password_length += 1
                up(1)
                print("*" * password_length)
                if password_attempt == names[username]:
                    break
                print("Wrong password please try again")
                pass_attempts += 1
        else:
            while True:
                print("Do you already have a Chatter account [Y]es or [N]o")
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
        
    user_name_getter()

    try:
        names = load(f"{os.environ['USERPROFILE']}/chatter/names.pk")
    except FileNotFoundError:
        names = {}

    save(names,f"{os.environ['USERPROFILE']}/chatter/names.pk")
    while True:
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
            print("type exit to exit the Chatter terminal")
        else:
            print(f'[red]Error:\n   "{cmd}"\nUndefinedCommandError: "{cmd}" is not defined: type "help" for avalible commands[red]')
            
            
            
            
            
except KeyboardInterrupt:
    quit()
