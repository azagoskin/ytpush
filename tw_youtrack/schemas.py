import dataclasses
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass(init=False)
class Config:
    url: str
    token: str
    issue_pattern: str

    def __init__(self, configuration: Dict[str, str]):
        fields = {field.name for field in dataclasses.fields(self)}

        for key, value in configuration.items():
            cleaned_key = key.replace('youtrack.', '')
            if cleaned_key in fields:
                setattr(self, cleaned_key, value)


class Colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


@dataclass
class TimeTrackingItemDC:
    issue_id: str
    date: int
    minutes: int
    annotation: Optional[str]
    type: Optional[int] = None

    def as_body(self) -> dict:
        body = {
            "date": self.date,
            "duration": {
                "minutes": self.minutes,
            },
        }

        if self.annotation:
            body["text"] = self.annotation
        if self.type:
            body["type"] = {
                "id": self.type
            }

        return body
