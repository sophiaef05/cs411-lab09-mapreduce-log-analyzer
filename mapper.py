"""
Lab 9: MapReduce Log Analyzer -- mapper.py starter.

Reads nginx-style access log lines from STDIN, one request per line,
e.g.: 127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /checkout HTTP/1.1" 200 512

For each line, extract the request path and write "<endpoint>\t1" to
stdout. See the assignment, Part B, for the full
requirements.
"""

import re
import sys

REQUEST_LINE_RE = re.compile(r'"[A-Z]+ (\S+) HTTP/')


def main() -> None:
    # TODO: for each line of sys.stdin, extract the endpoint and print "<endpoint>\t1"
    for line in sys.stdin:
        match = REQUEST_LINE_RE.search(line)
        if match:
            sys.stdout.write(f"{match.group(1)}\t1\n")


if __name__ == "__main__":
    main()
