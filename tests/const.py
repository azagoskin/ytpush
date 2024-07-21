TIMEWARRIOR_STDIN = r"""youtrack.issue_pattern: ^NONSTD-\d{2}$
youtrack.token: MYYOUTRACK_TOKEN
youtrack.url: https://youtrack.mysite.ru


[
{"id":32,"start":"20240715T075500Z","end":"20240715T081728Z","tags":["Meet","NONSTD-68"], "annotation":"дейлик"},
{"id":30,"start":"20240715T100059Z","end":"20240715T114820Z","tags":["Meet","NONSTD-68"],"annotation":"1-1"}
]
"""
TIMEWARRIOR_MULTIPLE_TAGS_STDIN = r"""youtrack.issue_pattern: ^NONSTD-\d{2}$
youtrack.token: MYYOUTRACK_TOKEN
youtrack.url: https://youtrack.mysite.ru


[
{"id":32,"start":"20240715T075500Z","end":"20240715T081728Z","tags":["Meet", "NONSTD-68","NONSTD-68"], "annotation":"дейлик"},
{"id":30,"start":"20240715T100059Z","end":"20240715T114820Z","tags":["Meet","NONSTD-68"],"annotation":"1-1"}
]
"""
TIMEWARRIOR_MULTIPLE_TYPES_STDIN = r"""youtrack.issue_pattern: ^NONSTD-\d{2}$
youtrack.token: MYYOUTRACK_TOKEN
youtrack.url: https://youtrack.mysite.ru


[
{"id":32,"start":"20240715T075500Z","end":"20240715T081728Z","tags":["Meet", "NONSTD-68"], "annotation":"дейлик"},
{"id":30,"start":"20240715T100059Z","end":"20240715T114820Z","tags":["Meet", "Development", "NONSTD-68"],"annotation":"1-1"}
]
"""
TIMEWARRIOR_NOT_FOUND_STDIN = r"""youtrack.issue_pattern: ^NONSTD-\d{2}$
youtrack.token: MYYOUTRACK_TOKEN
youtrack.url: https://youtrack.mysite.ru


[
{"id":32,"start":"20240715T075500Z","end":"20240715T081728Z","tags":["Meet", "NONSTD-69"], "annotation":"дейлик"}
]
"""
