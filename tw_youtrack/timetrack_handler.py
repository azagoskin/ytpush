import json
import re
from typing import Dict, List
from datetime import datetime

from tw_youtrack.schemas import TimeTrackingItemDC

DATEFORMAT = "%Y%m%dT%H%M%SZ"
TAG_HEADER = "tags"
ANNOTATION_HEADER = "annotation"
START_HEADER = "start"
END_HEADER = "end"


def convert_datetimes(start: str, end: str):
    start_dt = datetime.strptime(start, DATEFORMAT)
    end_dt = datetime.strptime(end, DATEFORMAT)
    interval = end_dt - start_dt
    minutes = interval.seconds // 60 if interval.seconds > 60 else 1
    epoch_time = int(end_dt.timestamp() * 1000)
    return minutes, epoch_time


def parse_timewarrior_timetrack(
        issue_id: str,
        timetrack: Dict[str, str],
        valid_types: Dict[str, str]
) -> TimeTrackingItemDC:
    timetrack_type = None
    minutes, epoch_time = convert_datetimes(
        timetrack.get(START_HEADER),
        timetrack.get(END_HEADER)
    )

    for tag in timetrack.get(TAG_HEADER):
        if tag != issue_id and tag in valid_types:
            timetrack_type = valid_types[tag]

    timetrack = TimeTrackingItemDC(
        issue_id=issue_id,
        annotation=timetrack.get(ANNOTATION_HEADER),
        minutes=minutes,
        date=epoch_time,
        type=timetrack_type
    )

    return timetrack


def parse_timewarrior_body(
        tw_body: str, valid_types: Dict[str, str], issue_pattern: str
) -> List[TimeTrackingItemDC]:
    timetracks: List[TimeTrackingItemDC] = []
    raw_timetracks = json.loads(tw_body)

    for raw_timetrack in raw_timetracks:
        for tag in raw_timetrack.get(TAG_HEADER):
            if re.search(issue_pattern, tag):
                timetracks.append(
                    parse_timewarrior_timetrack(
                        tag, raw_timetrack, valid_types
                    )
                )

    return timetracks
