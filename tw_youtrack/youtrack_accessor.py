import json

from http.client import HTTPSConnection, HTTPResponse
from urllib.parse import urlencode

from tw_youtrack.logger import Logger
from tw_youtrack.schemas import TimeTrackingItemDC, Config


class YoutrackAccessor:
    HEADERS = {
        "Accept": "application/json",
        "Cache-control": "no-cache",
        "Content-Type": "application/json",
    }
    ENDPOINTS = {
        "check_connection": "/api/users/me",
        "get_work_item_types": "/api/admin/timeTrackingSettings/workItemTypes",
        "get_issue": "/api/issues/",
        "load_timetrack": "/timeTracking/workItems",
    }

    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.url = config.url.replace("https://", "")
        self.HEADERS["Authorization"] = f"Bearer {config.token}"

    def get_request(self, endpoint: str) -> HTTPResponse:
        connection = HTTPSConnection(self.url)
        connection.request("GET", endpoint, headers=self.HEADERS)
        return connection.getresponse()

    def post_request(self, endpoint: str, body: str) -> HTTPResponse:
        connection = HTTPSConnection(self.url)
        connection.request("POST", endpoint, body=body, headers=self.HEADERS)
        return connection.getresponse()

    def check_connection(self) -> None:
        response = self.get_request(self.ENDPOINTS["check_connection"])
        self.logger(f"Connection to {self.url}", response.status == 200)

    def set_work_item_types(self) -> None:
        params = urlencode({"fields": "id,name"}, safe=",")
        url = f'{self.ENDPOINTS["get_work_item_types"]}?{params}'
        response = self.get_request(url)
        self.config.valid_types = {
            item["name"]: item["id"] for item in json.loads(response.read())
        }
        self.logger("Load work item types", response.status == 200)

    def check_issue(self, timetrack: TimeTrackingItemDC) -> None:
        url = self.ENDPOINTS["get_issue"] + timetrack.issue_name
        response = self.get_request(url)
        self.logger(f"Check issue {timetrack.issue_name}", response.status == 200)

    def load_time_track(self, timetrack: TimeTrackingItemDC) -> None:
        response = self.post_request(
            self.ENDPOINTS["get_issue"]
            + timetrack.issue_name
            + self.ENDPOINTS["load_timetrack"],
            body=json.dumps(timetrack.as_body()),
        )
        self.logger(
            f"Track {timetrack.minutes} mins to {timetrack.issue_name}",
            response.status == 200,
        )
