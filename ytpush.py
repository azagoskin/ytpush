#!/usr/bin/python3
import sys

from tw_youtrack.timetrack_handler import parse_timewarrior_body
from tw_youtrack.youtrack_accessor import YoutrackAccessor


def parse_tw_output(input_stream):
    header = 1
    configuration = dict()
    body = ""
    for line in input_stream:
        if header:
            if line == "\n":
                header = 0
            else:
                fields = line.strip().split(": ", 2)
                if len(fields) == 2:
                    configuration[fields[0]] = fields[1]
                else:
                    configuration[fields[0]] = ""
        else:
            body += line

    return configuration, body


if __name__ == "__main__":
    config, raw_timetracks = parse_tw_output(sys.stdin)

    yt_accessor = YoutrackAccessor(
        url=config["youtrack.url"],
        token=config["youtrack.token"]
    )

    yt_accessor.check_connection()
    valid_types = yt_accessor.get_work_item_types()
    timetracks = parse_timewarrior_body(
        raw_timetracks, valid_types, config["youtrack.issue_pattern"]
    )

    for timetrack in timetracks:
        yt_accessor.check_issue(timetrack)
        # yt_accessor.load_time_track(timetrack)
