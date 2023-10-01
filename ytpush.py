#!/usr/bin/python3
import sys
from typing import Tuple, Dict

from tw_youtrack.schemas import Config
from tw_youtrack.timetrack_handler import parse_timewarrior_body
from tw_youtrack.youtrack_accessor import YoutrackAccessor


def parse_tw_output(input_stream) -> Tuple[Dict[str, str], str]:
    body = ""
    headers = dict()
    header = True

    for line in input_stream:
        if header:
            if line == "\n":
                header = False
            else:
                fields = line.strip().split(": ", 2)
                if len(fields) == 2:
                    headers[fields[0]] = fields[1]
                else:
                    headers[fields[0]] = ""
        else:
            body += line

    return headers, body


if __name__ == "__main__":
    summary_time = 0
    configuration, raw_timetracks = parse_tw_output(sys.stdin)
    
    config = Config(configuration)
    yt_accessor = YoutrackAccessor(config)

    yt_accessor.check_connection()
    valid_types = yt_accessor.get_work_item_types()

    timetracks = parse_timewarrior_body(
        raw_timetracks, valid_types, config.issue_pattern
    )

    for timetrack in timetracks:
        yt_accessor.check_issue(timetrack)
        yt_accessor.load_time_track(timetrack)
        summary_time += timetrack.minutes

    print(f"Summary: {summary_time}mins")
