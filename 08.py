"""🎄 Solution for Day 8 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 08.py
"""

inp = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
part1_asserts = [
    (inp, 40),
]
part2_asserts = [
    (inp, 25272),
]


def distance(a, b) -> int:
    r = 0
    for a_xyz, b_xyz in zip(a, b):
        r += (b_xyz - a_xyz) * (b_xyz - a_xyz)
    return r


def part1(inp: str) -> int:
    coords = [
        tuple(int(i) for i in line.split(",")) for line in inp.strip().split("\n")
    ]
    connection_amount = 1000 if len(coords) > 20 else 10
    pairs = [(a, b) for a in range(len(coords)) for b in range(a + 1, len(coords))]
    shortest_pairs = sorted(pairs, key=lambda p: distance(coords[p[0]], coords[p[1]]))[
        :connection_amount
    ]

    groups = []
    for pair in shortest_pairs:
        pair = set(pair)
        new_set = pair
        new_groups = []
        for group in groups:
            if pair & group:
                new_set = new_set | group
            else:
                new_groups.append(group)
        new_groups.append(new_set)
        groups = new_groups

    group_sizes = [len(group) for group in groups]
    r = 1
    for size in sorted(group_sizes)[-3:]:
        r *= size
    return r


def part2(inp: str) -> int | None:
    coords = [
        tuple(int(i) for i in line.split(",")) for line in inp.strip().split("\n")
    ]
    pairs = [(a, b) for a in range(len(coords)) for b in range(a + 1, len(coords))]
    shortest_pairs = sorted(pairs, key=lambda p: distance(coords[p[0]], coords[p[1]]))

    groups = []
    for pair in shortest_pairs:
        a, b = pair
        pair = set(pair)
        new_set = pair
        new_groups = []
        for group in groups:
            if pair & group:
                new_set = new_set | group
            else:
                new_groups.append(group)
        if len(new_set) == len(coords):
            return coords[a][0] * coords[b][0]
        new_groups.append(new_set)
        groups = new_groups

    return None
