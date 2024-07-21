import json
from typing import Optional, Dict, Union, Any

from requests import Response, request

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
        self.HEADERS["Authorization"] = f"Bearer {config.token}"

    def auth_request(
        self,
        path: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> "Response":
        return request(
            method=method,
            url=self.config.url + path,
            headers=self.HEADERS,
            params=params,
            json=body,
        )

    def check_connection(self) -> None:
        response = self.auth_request(self.ENDPOINTS["check_connection"])
        self.logger(
            f"Connection to {self.config.url}", response.status_code == 200
        )

    def set_work_item_types(self) -> None:
        params = {"fields": "id,name"}
        response = self.auth_request(
            self.ENDPOINTS["get_work_item_types"], params=params
        )
        self.config.valid_types = {
            item["name"]: item["id"] for item in json.loads(response.text)
        }
        self.logger("Load work item types", response.status_code == 200)

    def check_issue(self, timetrack: TimeTrackingItemDC) -> None:
        url = self.ENDPOINTS["get_issue"] + timetrack.issue_name
        response = self.auth_request(url)
        self.logger(
            f"Check issue {timetrack.issue_name}", response.status_code == 200
        )

    def load_time_track(self, timetrack: TimeTrackingItemDC) -> None:
        params = {"fields": "date,duration(id,minutes),text,type(id,name)"}
        response = self.auth_request(
            self.ENDPOINTS["get_issue"]
            + timetrack.issue_name
            + self.ENDPOINTS["load_timetrack"],
            method="POST",
            params=params,
            body=timetrack.as_body(),
        )
        self.logger(
            f"Track {timetrack.minutes} mins to {timetrack.issue_name}",
            response.status_code == 200,
        )
