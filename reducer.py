"""
Lab 9: MapReduce Log Analyzer -- reducer.py starter.

Reads tab-separated "<endpoint>\t1" pairs from STDIN, PRE-SORTED by
endpoint (that's what the `sort` in the pipeline is for -- this is
what lets you accumulate one key at a time instead of loading
everything into memory). On each key change, print the finished
"<endpoint>\t<total_count>" for the PREVIOUS key. After the reduce
pass, sort the accumulated (endpoint, count) results descending by
count -- ties broken by endpoint name ascending, for determinism --
and print only the top 10.

See the assignment, Part B, for the full
requirements.
"""

import sys


def main() -> None:
    # TODO:
    # 1. Stream sys.stdin line by line (do not read it all into a list at once).
    #    Split each line on the tab into (endpoint, _). Track a
    #    "current_endpoint" and "current_count" as you go; when the
    #    endpoint changes, that's a completed group -- record it.
    # 2. After the stream ends, sort the completed (endpoint, count) groups:
    #    descending by count, ties broken by endpoint ascending.
    # 3. Print only the top 10, each as "<endpoint>\t<count>".
    results = []
    current_endpoint = None
    current_count = 0

    for line in sys.stdin:
        parts = line.rstrip("\n").split("\t")
        if len(parts) != 2:
            continue
        endpoint, value = parts
        try:
            count = int(value)
        except ValueError:
            continue

        if endpoint == current_endpoint:
            current_count += count
        else:
            if current_endpoint is not None:
                results.append((current_endpoint, current_count))
            current_endpoint = endpoint
            current_count = count

    if current_endpoint is not None:
        results.append((current_endpoint, current_count))

    results.sort(key=lambda kv: (-kv[1], kv[0]))

    for endpoint, count in results[:10]:
        sys.stdout.write(f"{endpoint}\t{count}\n")


if __name__ == "__main__":
    main()
