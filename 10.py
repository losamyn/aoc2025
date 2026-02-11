"""🎄 Solution for Day 10 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 10.py
"""

inp = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
inp2 = """[.#...#] (2,4) (3,4) (0,2,3,5) (0,1,2,3) (1,3,4,5) {26,32,28,47,23,20}
"""
part1_asserts = [
    (inp, 7),
]
part2_asserts = [
    (inp, 33),
    (inp2, 49),
    (inp2, 0),
]


def parse_line(line):
    goal, *buttons, joltage = line.split()
    goal = [c == "#" for c in goal.strip("[]")]
    buttons = [tuple(map(int, button.strip("()").split(","))) for button in buttons]
    joltage = list(map(int, joltage.strip("{}").split(",")))
    return goal, buttons, joltage


def calculate_steps(goal, buttons):
    # Work backwards, start with the goal and try to get to all False
    state = list(goal)
    current_buttons = set(buttons)
    queue = [(state, current_buttons)]
    while len(queue):
        state, current_buttons = queue.pop(0)
        if not any(state):
            # state is all False, found solution
            return len(buttons) - len(current_buttons)
        # Find buttons for the indicator that has least available buttons to press
        buttons_to_press = current_buttons
        for i, indicator in enumerate(state):
            if indicator:
                filtered_buttons = [button for button in current_buttons if i in button]
                if len(filtered_buttons) < len(buttons_to_press):
                    buttons_to_press = filtered_buttons
        # Press all the buttons found prior and add them to queue
        for button in buttons_to_press:
            new_state = list(state)
            for ind in button:
                new_state[ind] = not new_state[ind]
            queue.append((new_state, current_buttons - {button}))
    print("Failed to find solution for: ", goal)
    return 0


def calculate_steps_two(goal, buttons):
    # Approach: get state to all zeroes and keep track of which buttons are used for it
    state = list(goal)
    steps = {button: 0 for button in buttons}
    sorted_buttons = sorted(buttons, key=len, reverse=True)
    while len(sorted_buttons):
        # Update available buttons
        buttons_by_counter = {counter: [] for counter in range(len(state))}
        for button in list(sorted_buttons):
            if all([state[c] > 0 for c in button]):
                for c in button:
                    buttons_by_counter[c].append(button)
            else:
                sorted_buttons.remove(button)
        if not len(sorted_buttons):
            break
        # Select next button
        next_button = None
        for buttons_for_c in buttons_by_counter.values():
            if len(buttons_for_c) == 1:
                next_button = buttons_for_c[0]
                break
        else:
            next_button = sorted_buttons[0]
        # Press the button as many times as possible
        available_presses = min([state[c] for c in next_button])
        for c in next_button:
            state[c] -= available_presses
        steps[next_button] += available_presses
    if any(state):
        print("Joltages not complete for:")
        print(goal, "-- Final state:", state, steps, "-- sum:", sum(steps.values()))
        # return None
    return sum(steps.values())


def part1(inp: str) -> int:
    result = 0
    for line in inp.strip().split("\n"):
        goal, buttons, _ = parse_line(line)
        result += calculate_steps(goal, buttons)
    return result


def part2(inp: str) -> int:
    result = 0
    for line in inp.strip().split("\n"):
        _, buttons, goal = parse_line(line)
        result += calculate_steps_two(goal, buttons)
    return result
