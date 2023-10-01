import json
import sys
from http.client import HTTPSConnection, HTTPResponse
from urllib.parse import urlencode

from tw_youtrack.schemas import Colors, TimeTrackingItemDC, Config


class YoutrackAccessor:
    HEADERS = {
        "Accept": "application/json",
        "Cache-control": "no-cache",
        "Content-Type": "application/json"
    }
    ENDPOINTS = {
        "check_connection": "/api/users/me",
        "get_work_item_types": "/api/admin/timeTrackingSettings/workItemTypes",
        "get_issue": "/api/issues/",
        "load_timetrack": "/timeTracking/workItems"
    }

    def __init__(self, config: Config):
        self.url = config.url.replace("https://", "")
        self.HEADERS["Authorization"] = f"Bearer {config.token}"

    @staticmethod
    def log(message: str, status_code: int):
        if status_code == 200:
            print(f"[{Colors.OKGREEN}OK{Colors.ENDC}] {message}")
        else:
            print(f"[{Colors.FAIL}FALSE{Colors.ENDC}] {message}")
            sys.exit(1)

    def get_request(self, endpoint: str) -> HTTPResponse:
        connection = HTTPSConnection(self.url)
        connection.request("GET", endpoint, headers=self.HEADERS)
        return connection.getresponse()

    def post_request(self, endpoint: str, body: str) -> HTTPResponse:
        connection = HTTPSConnection(self.url)
        connection.request("POST", endpoint, body=body, headers=self.HEADERS)
        return connection.getresponse()

    def check_connection(self):
        response = self.get_request(self.ENDPOINTS["check_connection"])
        self.log(f"Connection to {self.url}", response.status)

    def get_work_item_types(self):
        params = urlencode({"fields": "id,name"}, safe=",")
        url = f'{self.ENDPOINTS["get_work_item_types"]}?{params}'
        response = self.get_request(url)
        return {item["name"]: item["id"] for item in json.loads(response.read())}

    def check_issue(self, timetrack: TimeTrackingItemDC):
        url = self.ENDPOINTS["get_issue"] + timetrack.issue_id
        response = self.get_request(url)
        self.log(f"Check issue {timetrack.issue_id}", response.status)

    def load_time_track(self, timetrack: TimeTrackingItemDC):
        response = self.post_request(
            self.ENDPOINTS["get_issue"] + timetrack.issue_id
            + self.ENDPOINTS["load_timetrack"],
            body=json.dumps(timetrack.as_body()),
        )
        self.log(
            f"Track {timetrack.minutes} mins to {timetrack.issue_id}",
            response.status
        )
