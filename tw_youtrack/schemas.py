from dataclasses import dataclass
from typing import Optional


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