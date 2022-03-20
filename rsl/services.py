# Copyright 2022 iiPython

# Modules
import json
from time import sleep
from requests import get
from threading import Thread

# Tracker DB
class TrackerDB(object):
    def __init__(self) -> None:
        with open("db/current.json", "w+") as f:
            f.write("{}")

        self.data = {}

    def write(self, data: dict) -> None:
        self.data[data["id"]] = data
        with open("db/current.json", "w") as f:
            f.write(json.dumps(self.data, indent = 4))

# Tracking class
class ServiceTracker(object):
    def __init__(self) -> None:
        try:
            with open("config.json", "r") as cfg:
                self.services = json.loads(cfg.read())["services"]

        except Exception:
            self.services = []

        for service in self.services:
            Thread(target = self.track, args = [service]).start()

    def guess_status(self, service: dict, code: int, ping: int) -> str:
        if code != 200:
            return "down", "Non-200 status code"

        threshold = service.get("threshold", 500)
        if ping > threshold:
            return "slow", f"Ping higher than {threshold}ms threshold"

        elif ping > threshold + 100:
            return "down", f"Ping time exceeds {threshold + 100}ms"

        return "up", "No problems detected"

    def dump_tracker(self, data: dict) -> None:
        if not hasattr(self, "trackerdb"):
            self.trackerdb = TrackerDB()

        self.trackerdb.write(data)

    def track(self, service: dict) -> None:

        # Initialization
        service_url = f"https://{service['id']}.roblox.com/{service.get('endpoint', '')}"
        while True:
            try:
                req = get(service_url, timeout = service.get("timeout", 5))
                code, ping = req.status_code, round(req.elapsed.total_seconds() * 1000, 2)

            except Exception:
                code, ping = 0, 0

            self.dump_tracker(service | {"url": service_url, "code": code, "ping": ping, "guess": list(self.guess_status(service, code, ping))})
            sleep(60)
