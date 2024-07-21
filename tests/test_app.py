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
def test_app_success(requests_mock):
    app(TIMEWARRIOR_STDIN)

    history = requests_mock.request_history
    task1_data = json.loads(history[4].text)
    assert task1_data == {
        "date": 1721020648000,
        "duration": {"minutes": 22},
        "text": "дейлик",
        "type": {"id": "89-6"},
    }
    task2_data = json.loads(history[5].text)
    assert task2_data == {
        "date": 1721033300000,
        "duration": {"minutes": 107},
        "text": "1-1",
        "type": {"id": "89-6"},
    }


@pytest.mark.usefixtures("external_requests")
def test_app_wrong_params():
    with pytest.raises(AttributeError):
        assert app(TIMEWARRIOR_MULTIPLE_TAGS_STDIN)

    with pytest.raises(AttributeError):
        assert app(TIMEWARRIOR_MULTIPLE_TYPES_STDIN)

    with pytest.raises(SystemExit):
        assert app(TIMEWARRIOR_NOT_FOUND_STDIN)
