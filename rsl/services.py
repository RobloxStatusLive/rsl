# Copyright 2022 iiPython

# Modules
import os
import json
import time
from requests import get
from threading import Thread
from datetime import datetime

from ._logging import log
from .config import config

# Initialization
historical_folder = os.path.join(config.get("rsl.dataLocation"), "db/days")
if not os.path.isdir(historical_folder):
    os.makedirs(historical_folder)

# Tracker DB
class TrackerDB(object):
    def __init__(self, dump_at: int) -> None:
        self.dump_at = dump_at
        self.pre_dump = []

    def watch(self) -> None:
        log("tracker", "RSL service tracker started", "green")
        while True:
            if len(self.pre_dump) == self.dump_at:
                now = datetime.utcnow()
                date = now.strftime("%D").replace("/", "-")

                # Save data to our day file
                day_file = os.path.join(historical_folder, f"{date}.json")
                if not os.path.isfile(day_file):
                    day_data = []

                else:
                    with open(day_file, "r") as df:
                        day_data = json.loads(df.read())

                day_data.append({"time": time.time() * 1000, "data": self.pre_dump})
                with open(day_file, "w+") as df:
                    df.write(json.dumps(day_data))

                self.pre_dump = []
                log("tracker", f"Dumped to {date}.json and flushed RAM cache")

            time.sleep(5)  # No need to rip CPUs, considering our data dump should be wrote every 60s

    def write(self, data: dict) -> None:
        self.pre_dump.append(data)

# Tracking class
class ServiceTracker(object):
    def __init__(self) -> None:
        with open(os.path.join(config.get("rsl.dataLocation"), "services.json"), "r") as cfg:
            self.services = json.loads(cfg.read())

        # Start trackers
        self.trackerdb = TrackerDB(len(self.services))
        Thread(target = self.trackerdb.watch).start()
        for service in self.services:
            Thread(target = self.track, args = [service]).start()

        log("tracker", f"Spawned all {len(self.services)} tracking thread(s)", "green")

    def guess_status(self, service: dict, code: int, ping: int) -> str:
        if code != 200:
            return "down", "Non-200 status code"

        threshold = service.get("threshold", 500)
        if ping > threshold:
            return "slow", f"Ping higher than {threshold}ms threshold"

        elif ping > threshold + 100:
            return "down", f"Ping time exceeds {threshold + 100}ms"

        return "up", "No problems detected"

    def track(self, service: dict) -> None:

        # Initialization
        service_url = f"https://{service['id']}.roblox.com/{service.get('endpoint', '')}"
        while True:
            try:
                req = get(service_url, timeout = service.get("timeout", 5))
                code, ping = req.status_code, round(req.elapsed.total_seconds() * 1000, 2)

            except Exception:
                code, ping = 0, 0

            self.trackerdb.write(service | {"url": service_url, "code": code, "ping": ping, "guess": list(self.guess_status(service, code, ping))})
            time.sleep(60)
