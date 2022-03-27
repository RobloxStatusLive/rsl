# Copyright 2022 iiPython

# Modules
import os
import time
import json
from typing import Tuple
from datetime import datetime, timedelta

from ._logging import log
from .config import config

# Database loader
class DBLoader(object):
    def __init__(self) -> None:
        self.historical_folder = os.path.join(config.get("rsl.dataLocation"), "db/days")
        self.service_cache = {}

    def gen_date(self) -> str:
        return datetime.utcnow().strftime("%D").replace("/", "-")

    def get_date_all(self, date: str) -> list:
        date_file = os.path.join(self.historical_folder, f"{date}.json")
        if not os.path.isfile(date_file):
            log("reader", f"No data stored for {date}, returning previous day ...", "yellow")
            return self.get_date_all((datetime.utcnow() - timedelta(days = 1)).strftime("%D").replace("/", "-"))

        with open(date_file, "r") as df:
            latest = json.loads(df.read())

        return latest

    def get_date_min(self, date: str) -> list:
        return sorted(self.get_date_all(date)[-1]["data"], key = lambda s: s["name"])

    def get_current(self) -> list:
        return self.get_date_min(self.gen_date())

    def get_service_data(self, service_id: str, date: str = None, cache: bool = True) -> Tuple[str, dict, float]:
        if date is None:
            date = self.gen_date()

        if cache:
            if service_id in self.service_cache and date in self.service_cache[service_id]:
                if self.service_cache[service_id][date][0] > time.time():
                    return self.service_cache[service_id][date][1]

                del self.service_cache[service_id][date]
                if not self.service_cache[service_id]:
                    del self.service_cache[service_id]

        data = self.get_date_all(date)
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
            log("cache", f"Cached service '{service_id}' ({date}) for 5 minutes")
            if service_id not in self.service_cache:
                self.service_cache[service_id] = {}

            self.service_cache[service_id][date] = (time.time() + 300, results)

        return results

    def guess_status(self, data: list) -> tuple:
        slow = [s for s in data if s["guess"][0] == "slow"]
        down = [s for s in data if s["guess"][0] == "down"]
        return ("down", "red") if len(down) > 3 else (("partially down", "yellow") if len(slow) > 3 else ("online", "green"))
