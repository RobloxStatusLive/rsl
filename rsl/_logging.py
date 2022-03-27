# Copyright 2022 iiPython

# Modules
import os
import logging
from iipython import color
from datetime import datetime

from .config import config

# Initialization
logging.getLogger("werkzeug").setLevel(logging.ERROR)  # No need for request logs
log_directory = os.path.join(config.get("rsl.dataLocation"), "logs")

# Logging handler
def pad(text: str) -> None:
    return f"{text}{' ' * (20 - len(text))}"

def write(text: str) -> None:
    if not os.path.isdir(log_directory):
        os.mkdir(log_directory)  # Create the log directory

    file = os.path.join(log_directory, datetime.now().strftime("%D").replace("/", "-") + ".log")
    with open(file, "a") as lf:
        lf.write(text + "\n")

def log(level: str, message: str, pcolor: str = "blue") -> None:
    time = datetime.now().strftime("%m/%d/%Y, %I:%M %p")
    result = f"[cyan]{pad(time)} | [yellow]{pad(level.upper())} | [{pcolor}]{message}"

    # Handle logging
    print(color(result, dry = not config.get("logging.useColor")))
    if config.get("logging.dumpToFile"):
        write(color(result, dry = True))
