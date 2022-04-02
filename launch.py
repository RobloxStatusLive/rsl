# Copyright 2022 iiPython
# Roblox Status Live

# Modules
from rsl import app

# Launch server
if __name__ == "__main__":
    app.run(
        host = "0.0.0.0",
        port = 8080, # Change to 80 for HTTP
        debug = True
    )
