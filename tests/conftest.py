import os
import pytest
import json
from typing import Any

BASE_URL = "https://youtrack.mysite.ru/api"
DATA_DIR = "tests/data"


def read_file(filename: str) -> str:
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return f.read()


def read_json(filename: str) -> Any:
    return json.loads(read_file(filename))


@pytest.fixture
def external_requests(requests_mock) -> None:  # type: ignore
    requests_mock.get(BASE_URL + "/users/me", json=read_json("me.body.json"))
    requests_mock.get(
        BASE_URL + "/admin/timeTrackingSettings/workItemTypes",
        json=read_json("itemTypes.body.json"),
    )
    requests_mock.get(
        BASE_URL + "/issues/NONSTD-68", json=read_json("issues.body.json")
    )
    requests_mock.get(
        BASE_URL + "/issues/NONSTD-69",
        json=read_json("issues_404.body.json"),
        status_code=404,
    )
    fields = "date,duration(id,minutes),text,type(id,name)"
    requests_mock.post(
        BASE_URL + f"/issues/NONSTD-68/timeTracking/workItems?fields={fields}",
        json=read_json("timeTracking.body.json"),
    )
