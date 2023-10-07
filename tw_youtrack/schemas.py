from __future__ import annotations
import json
import re
from dataclasses import dataclass, fields as dataclass_fields
from datetime import datetime
from typing import Dict, List, Optional, Sequence

__all__ = ("Config", "TimeTrackingItemDC")


DATEFORMAT = "%Y%m%dT%H%M%SZ"
TAG_HEADER = "tags"
ANNOTATION_HEADER = "annotation"
START_HEADER = "start"
END_HEADER = "end"


@dataclass(init=False)
class Config:
    url: str
    token: str
    issue_pattern: str
    username: str
    valid_types: Dict[str, str]

    def __init__(self, raw_configuration: str):
        fields = {field.name for field in dataclass_fields(self)}

        for line in raw_configuration.split('\n'):
            key, value = line.split(": ")
            cleaned_key = key.replace('youtrack.', '')
            if cleaned_key in fields:
                setattr(self, cleaned_key, value)


@dataclass
class TimeTrackingItemDC:
    issue_name: str
    date: int
    minutes: int
    annotation: Optional[str]
    type: Optional[int]

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
            body["type"] = {"id": self.type}

        return body

    @staticmethod
    def _convert_datetimes(start: str, end: str):
        start_dt = datetime.strptime(start, DATEFORMAT)
        end_dt = datetime.strptime(end, DATEFORMAT)
        interval = end_dt - start_dt
        minutes = interval.seconds // 60 if interval.seconds > 60 else 1
        epoch_time = int(end_dt.timestamp() * 1000)
        return minutes, epoch_time

    @staticmethod
    def _get_issue_id(tags: Sequence[str], pattern: str) -> Optional[str]:
        ids = [tag for tag in tags if re.search(pattern, tag)]
        if len(ids) > 1:
            raise Exception(f"More than one tag: {ids}")

        return ids[0] if ids else None

    @staticmethod
    def _get_issue_type(tags: Sequence[str], valid_types: Dict) -> Optional[str]:
        types = [valid_types[tag] for tag in tags if tag in valid_types]
        if len(types) > 1:
            raise Exception(f"More than one type: {types}")

        return types[0] if types else None

    @classmethod
    def load_many(cls, tw_body: str, config: Config) -> List[TimeTrackingItemDC]:
        timetracks: List[TimeTrackingItemDC] = []

        for raw_timetrack in json.loads(tw_body):
            tags = raw_timetrack.get(TAG_HEADER, ())
            issue_name = cls._get_issue_id(tags, config.issue_pattern)
            timetrack_type = cls._get_issue_type(tags, config.valid_types)
            minutes, epoch_time = cls._convert_datetimes(
                raw_timetrack.get(START_HEADER),
                raw_timetrack.get(END_HEADER)
            )

            if issue_name:
                timetracks.append(
                    cls(
                        issue_name=issue_name,
                        annotation=raw_timetrack.get(ANNOTATION_HEADER),
                        minutes=minutes,
                        date=epoch_time,
                        type=timetrack_type
                    )
                )

        return timetracks
