"""🎄 Solution for Day 10 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 10.py
"""

from collections import deque

inp = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
part1_asserts = [
    (inp, 7),
]
part2_asserts = [
    (inp, 33),
]


def parse_line(line):
    goal, *switches, joltage = line.split()
    goal = [c == "#" for c in goal.strip("[]")]
    switches = [tuple(map(int, switch.strip("()").split(","))) for switch in switches]
    joltage = list(map(int, joltage.strip("{}").split(",")))
    return goal, switches, joltage


def calculate_steps(goal, switches):
    initial_state = [False] * len(goal)
    initial_steps = 0
    initial_switches = set(switches)
    queue = deque([(initial_state, initial_steps, initial_switches)])
    while len(queue) > 0:
        state, steps, possible_switches = queue.popleft()
        for switch in possible_switches:
            # Toggle the switch
            new_state = list(state)  # Need to make a copy of previous state
            new_switches = possible_switches - {switch}
            for i in switch:
                new_state[i] = not state[i]
            # Check if goal is reached
            if new_state == goal:
                return steps + 1
            elif len(new_switches) > 0:
                # Put new possible state in the queue
                queue.append((new_state, steps + 1, new_switches))
    # Should never get to this path if input is correct
    print("Unable to find solution for:")
    print(goal, switches)
    return 0


def calculate_steps_two(goal, switches):
    initial_state = [0] * len(goal)
    initial_steps = 0
    initial_switches = set(switches)
    queue = deque([(initial_state, initial_steps, initial_switches)])
    while len(queue) > 0:
        state, steps, possible_switches = queue.popleft()
        for switch in possible_switches:
            # Activate the switch
            new_state = list(state)  # Need to make a copy of previous state
            new_switches = set(possible_switches)
            for i in switch:
                new_state[i] += 1
                # Remove all possible switches that contain this index
                if new_state[i] >= goal[i]:
                    for s in possible_switches:
                        if i in s:
                            new_switches.discard(s)
            # Check if goal is reached
            if new_state == goal:
                return steps + 1
            # if all(s <= g for s, g in zip(new_state, goal)):
            #     # Put new possible state in the queue if all joltages are at or below goal
            #     new_switches = possible_switches - {switch}
            queue.append((new_state, steps + 1, new_switches))
    # Should never get to this path if input is correct
    print("Unable to find solution for:")
    print(goal, switches)
    return 0


def part1(inp: str) -> int:
    result = 0
    for line in inp.strip().split("\n"):
        goal, switches, _ = parse_line(line)
        result += calculate_steps(goal, switches)
    return result


def part2(inp: str) -> int:
    result = 0
    for line in inp.strip().split("\n"):
        _, switches, goal = parse_line(line)
        result += calculate_steps_two(goal, switches)
    return result
