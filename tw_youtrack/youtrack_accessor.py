import json
import sys
import requests

from tw_youtrack.schemas import Colors, TimeTrackingItemDC


class YoutrackAccessor:
    HEADERS = {
        "Accept": "application/json",
        "Cache-control": "no-cache",
        "Content-Type": "application/json"
    }
    ENDPOINTS = {
        "check_connection": "/users/me",
        "get_work_item_types": "/admin/timeTrackingSettings/workItemTypes",
        "get_issue": "/issues/",
        "load_timetrack": "/timeTracking/workItems"
    }

    def __init__(self, url, token):
        self.url = url
        self.HEADERS["Authorization"] = f"Bearer {token}"

    def log(self, message: str, status_code: int):
        if status_code == 200:
            print(f"[{Colors.OKGREEN}OK{Colors.ENDC}] {message}")
        else:
            print(f"[{Colors.FAIL}FALSE{Colors.ENDC}] {message}")
            sys.exit(1)

    def check_connection(self):
        response = requests.get(
            self.url + self.ENDPOINTS["check_connection"],
            headers=self.HEADERS
        )
        self.log(f"Connection to {self.url}", response.status_code)

    def get_work_item_types(self):
        payload = {"fields": "id,name"}
        response = requests.get(
            self.url + self.ENDPOINTS["get_work_item_types"],
            headers=self.HEADERS,
            params=payload
        )

        valid_types = {item["name"]: item["id"] for item in response.json()}

        self.log(
            f"Get work item types ({list(valid_types.keys())})",
            response.status_code
        )

        return valid_types

    def check_issue(self, timetrack: TimeTrackingItemDC):
        response = requests.get(
            self.url + self.ENDPOINTS["get_issue"] + timetrack.issue_id,
            headers=self.HEADERS,
        )
        self.log(f"Check issue {timetrack.issue_id}", response.status_code)

    def load_time_track(self, timetrack: TimeTrackingItemDC):
        response = requests.post(
            self.url + self.ENDPOINTS["get_issue"] +
            timetrack.issue_id + self.ENDPOINTS["load_timetrack"],
            headers=self.HEADERS,
            data=json.dumps(timetrack.as_body())
        )
        self.log(
            f"Track {timetrack.minutes} mins to {timetrack.issue_id}",
            response.status_code
        )
