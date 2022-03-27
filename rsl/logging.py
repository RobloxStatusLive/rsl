# Copyright 2022 iiPython

# Modules
import os
import logging
from iipython import color
from datetime import datetime

# Initialization
logging.getLogger("werkzeug").setLevel(logging.ERROR)  # No need for request logs
log_directory = os.path.join(os.path.dirname(__file__), "../logs")
if not os.path.isdir(log_directory):
    os.mkdir(log_directory)  # Create the log directory

# Logging handler
def pad(text: str) -> None:
    return f"{text}{' ' * (20 - len(text))}"

def write(text: str) -> None:
    date = datetime.now().strftime("%D").replace("/", "-")
    file = os.path.join(log_directory, date + ".log")
    with open(file, "a") as lf:
        lf.write(text + "\n")

def log(level: str, message: str, pcolor: str = "blue") -> None:
    time = datetime.now().strftime("%m/%d/%Y, %I:%M %p")
    result = f"[cyan]{pad(time)} | [yellow]{pad(level.upper())} | [{pcolor}]{message}"

    # Handle logging
    print(color(result))
    write(color(result, dry = True))
