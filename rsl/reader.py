# Copyright 2022 iiPython

# Modules
import os
import time
import json
from time import sleep
from typing import Tuple
from datetime import datetime

# Database loader
class DBLoader(object):
    def __init__(self) -> None:
        self.day_db = os.environ.get("_RSL_DAY_DB")
        while not self.day_db:
            self.day_db = os.environ.get("_RSL_DAY_DB")
            print("[LOADER] Awaiting for _RSL_DAY_DB environ to be set (2s) ...")
            sleep(2)

        self.service_cache = {}

    def gen_date(self) -> str:
        return datetime.utcnow().strftime("%D").replace("/", "-")

    def get_date_all(self, date: str) -> list:
        date_file = os.path.join(self.day_db, f"{date}.json")
        with open(date_file, "r") as df:
            latest = json.loads(df.read())

        return latest

    def get_date_min(self, date: str) -> list:
        return sorted(self.get_date_all(date)[-1]["data"], key = lambda s: s["name"])

    def get_current(self) -> list:
        return self.get_date_min(self.gen_date())

    def get_service_data(self, service_id: str, cache: bool = True) -> Tuple[str, dict, float]:
        if cache:
            if service_id in self.service_cache:
                if self.service_cache[service_id][0] > time.time():
                    print(f"[CACHE] Got a hit for service '{service_id}', replied from cache")
                    return self.service_cache[service_id][1]

                del self.service_cache[service_id]

        data = self.get_date_all(self.gen_date())
        name, points, down = None, {}, 0
        for point in data:
            for service in point["data"]:
                if service["id"] == service_id:
                    if service["guess"][0] in ["slow", "down"]:
                        down += 1

                    name = service["name"]
                    points[point["time"]] = service["ping"]

        results = (name, points, round((len(points) - down) / len(points), 2) * 100)
        if cache:
            print(f"[CACHE] Got a hit for service '{service_id}', response has been cached")
            self.service_cache[service_id] = (time.time() + 300, results)

        return results

    def guess_status(self, data: list) -> tuple:
        slow = [s for s in data if s["guess"][0] == "slow"]
        down = [s for s in data if s["guess"][0] == "down"]
        return ("down", "red") if len(down) > 3 else (("partially down", "yellow") if len(slow) > 3 else ("online", "green"))
