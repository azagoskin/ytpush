# TimeWarrior YouTrack Push
## Summary
**ytpush** - [TimeWarrior](https://timewarrior.net/docs/api/) extension for uploading timelog to YouTrack. Task URLs and types (review, documentation, development, etc.) are taken from tags.

Interval intersections are not tracked
## Installation
Copy the files to the directory `~/.timewarrior/extensions`:
```
$ ls -la ~/.timewarrior/extensions/
drwx------ 6 4096 окт  1 21:12 .
drwx------ 5 4096 окт  1 14:50 ..
drwxr-xr-x 3 4096 окт  1 21:19 tw_youtrack
-rwxr--r-- 1 1340 окт  1 21:12 ytpush.py
```
```
$ sudo chmod 744 ytpush.py
```
## Configuration
Add parameters to the `~/.timewarrior/timewarrior.cfg`:
```
youtrack.token=perm:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
youtrack.url=youtrack.mysite.ru
youtrack.issue_pattern=^ABCD-\d{3,4}$
```
where `^ABCD-\d{3,4}$` is a regular expression for searching for the task name in tags
## Usage
Usage command example:
```
$ timew summary

Wk  Date       Day Tags                     Start      End    Time   Total
W39 2023-10-01 Sun Documentation, ABCD-4681 10:00:00 10:10:00 0:10:00 0:10:00

                                                                      0:10:00
$ timew ytpush 2023-10-01
[OK] Connection to youtrack.mysite.ru
[OK] Check issue ABCD-4681
[OK] Track 10 mins to ABCD-4681
Summary: 10mins
```
