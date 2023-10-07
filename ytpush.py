#!/usr/bin/python3
import sys

from tw_youtrack.logger import Logger
from tw_youtrack.schemas import Config, TimeTrackingItemDC
from tw_youtrack.youtrack_accessor import YoutrackAccessor


if __name__ == "__main__":
    summary_time = 0
    raw_configuration, raw_timetracks = sys.stdin.read().split('\n\n')

    config = Config(raw_configuration)
    logger = Logger()
    yt_accessor = YoutrackAccessor(config, logger)

    yt_accessor.check_connection()
    yt_accessor.set_work_item_types()

    timetracks = TimeTrackingItemDC.load_many(raw_timetracks, config)

    for timetrack in timetracks:
        yt_accessor.check_issue(timetrack)
        yt_accessor.load_time_track(timetrack)
        summary_time += timetrack.minutes

    logger(f"Summary: {summary_time}mins")
