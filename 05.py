"""🎄 Solution for Day 5 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 05.py
"""

inp = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
part1_asserts = [
    (inp, 3),
]
part2_asserts = [
    (inp, 14),
]


def compile_ranges(ranges):
    # takes a stream of ranges and returns an ordered list of non-overlapping ranges
    result = []
    for new in ranges:
        start_replace = 0
        stop_replace = 0
        for i, old in enumerate(result):
            if new[1] < old[0] - 1:
                break
            else:
                new[1] = max(new[1], old[1])
            if new[0] > old[1] + 1:
                start_replace = i + 1
            else:
                new[0] = min(new[0], old[0])
            stop_replace = i + 1

        result = result[:start_replace] + [new] + result[stop_replace:]

    return result


def part1(inp: str) -> int:
    ranges, ids = map(str.split, inp.split("\n\n"))
    ranges = compile_ranges(map(lambda r: list(map(int, r.split("-"))), ranges))
    ids = map(int, ids)
    result = 0
    for id in ids:
        for lower, upper in ranges:
            if lower <= id and id <= upper:
                result += 1
                break
    return result


def part2(inp: str) -> int:
    # Apologies for the oneliner
    ranges = map(lambda r: list(map(int, r.split("-"))), inp.split("\n\n")[0].split())
    compiled_ranges = compile_ranges(ranges)
    result = 0
    for lower, upper in compiled_ranges:
        result = result + upper - lower + 1

    return result
