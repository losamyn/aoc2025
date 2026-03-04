"""🎄 Solution for Day 11 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 11.py
"""

from functools import cache

inp = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""
inp2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""
part1_asserts = [
    (inp, 5),
]
part2_asserts = [
    (inp2, 2),
]


def part1(inp: str) -> int:
    graph = {
        node: connections.split()
        for node, connections in [line.split(": ") for line in inp.strip().split("\n")]
    }

    @cache
    def count_paths(start_node: str) -> int:
        if start_node == "out":
            return 1
        return sum(count_paths(node) for node in graph[start_node])

    return count_paths("you")


def part2(inp: str) -> int:
    graph = {
        node: connections.split()
        for node, connections in [line.split(": ") for line in inp.strip().split("\n")]
    }

    @cache
    def count_paths(start_node: str, visited_dac=False, visited_fft=False) -> int:
        if start_node == "out":
            return visited_dac and visited_fft
        if start_node == "dac":
            visited_dac = True
        elif start_node == "fft":
            visited_fft = True
        return sum(
            count_paths(node, visited_dac, visited_fft) for node in graph[start_node]
        )

    return count_paths("svr")
