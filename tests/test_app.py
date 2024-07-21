import pytest
import json

from tw_youtrack.app import app
from tests.const import (
    TIMEWARRIOR_STDIN,
    TIMEWARRIOR_MULTIPLE_TAGS_STDIN,
    TIMEWARRIOR_MULTIPLE_TYPES_STDIN,
    TIMEWARRIOR_NOT_FOUND_STDIN,
)


@pytest.mark.usefixtures("external_requests")
def test_app_success(requests_mock) -> None:  # type: ignore
    app(TIMEWARRIOR_STDIN)

    history = requests_mock.request_history
    assert history[4].headers["Authorization"] == "Bearer MYYOUTRACK_TOKEN"
    task1_data = json.loads(history[4].text)
    # TODO: fix timezone
    task1_data.pop("date")
    assert task1_data == {
        "duration": {"minutes": 22},
        "text": "дейлик",
        "type": {"id": "89-6"},
    }
    task2_data = json.loads(history[5].text)
    task2_data.pop("date")
    assert task2_data == {
        "duration": {"minutes": 107},
        "text": "1-1",
        "type": {"id": "89-6"},
    }


@pytest.mark.usefixtures("external_requests")
def test_app_wrong_params() -> None:
    with pytest.raises(AttributeError):
        app(TIMEWARRIOR_MULTIPLE_TAGS_STDIN)

    with pytest.raises(AttributeError):
        app(TIMEWARRIOR_MULTIPLE_TYPES_STDIN)

    with pytest.raises(SystemExit):
        app(TIMEWARRIOR_NOT_FOUND_STDIN)
