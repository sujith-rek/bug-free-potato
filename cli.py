import os
import subprocess
import readline
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Path to the history file
HISTORY_FILE = os.path.expanduser("history.txt")

# List of initialization scripts to run when the shell starts
INIT_SCRIPTS = [
    "H:\\all-languages.cmd",
]

# Load command history from the file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                readline.add_history(line.strip())

# Save command history to the file
def save_history():
    with open(HISTORY_FILE, "w") as f:
        for i in range(readline.get_current_history_length()):
            f.write(readline.get_history_item(i + 1) + "\n")

# Execute a command
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(Fore.RED + result.stderr)
    except Exception as e:
        print(Fore.RED + f"Error executing command: {e}")

# Execute initialization scripts
def run_init_scripts():
    print(Fore.CYAN + "Running initialization scripts...")
    for script in INIT_SCRIPTS:
        if os.path.exists(script):
            print(Fore.GREEN + f"Executing: {script}")
            execute_command(script)
        else:
            print(Fore.RED + f"Script not found: {script}")

# Custom commands logic
def custom_commands(command):
    if command.lower() == "ls":
        # Execute `dir` instead of `ls`
        execute_command("dir")
        return True
    elif command.lower() in ["clear", "cls"]:
        # Clear the terminal screen
        os.system("cls" if os.name == "nt" else "clear")
        return True
    return False

# Custom reverse search function
def reverse_search():
    print(Fore.CYAN + "\nReverse Search Mode: (Type your query and press Enter)")
    search_query = input(Fore.YELLOW + "Search: " + Style.RESET_ALL).strip()
    if not search_query:
        print(Fore.RED + "No query entered. Exiting reverse search.")
        return

    found = False
    try:
        for i in range(readline.get_current_history_length(), 0, -1):
            history_item = readline.get_history_item(i)
            if history_item and search_query in history_item:
                print(Fore.GREEN + f"Found: {history_item}")
                found = True
                break
        if not found:
            print(Fore.YELLOW + "No matching command found.")
    except Exception as e:
        print(Fore.RED + f"Error during reverse search: {e}")

# Main function
def main():
    print(Fore.CYAN + "Custom Shell (type 'exit' to quit)")
    load_history()

    # Run initialization scripts
    run_init_scripts()

    try:
        while True:
            try:
                # Input prompt
                command = input(Fore.YELLOW + "(❁´◡`❁) >>> " + Style.RESET_ALL)
                if command.strip() == "":
                    continue

                if command.lower() == "exit":
                    print(Fore.CYAN + "Exiting shell.")
                    break

                # Execute custom commands or system command
                if not custom_commands(command):
                    execute_command(command)
            except KeyboardInterrupt:
                print(Fore.CYAN + "\nExiting shell.")
                break
    finally:
        save_history()

if __name__ == "__main__":
    main()
