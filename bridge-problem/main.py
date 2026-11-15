import heapq
from itertools import count


def crossing_groups(bank_side) -> list[tuple[int, ...]]:
    singles = [(a,) for a in bank_side]
    pairs = [(a, b) for a in bank_side for b in bank_side if a < b]
    return singles + pairs


def next_states(state, everyone, times) -> list[tuple[int, tuple[frozenset[int], int], tuple[str, tuple[int, ...]]]]:
    left, side = state
    bank_side = left if side == 0 else everyone - left
    arrow = "->" if side == 0 else "<-"
    states = []

    for group in crossing_groups(bank_side):
        g = frozenset(group)
        new_left = left - g if side == 0 else left | g
        states.append(
            (max(times[p] for p in group), (new_left, 1 - side), (arrow, group))
        )

    return states


def bridge_problem(minutes_to_cross) -> tuple[float, list]:
    times = {i + 1: m for i, m in enumerate(minutes_to_cross)}
    everyone = frozenset(times)

    tie = count()
    priority_queue = [(0, next(tie), (everyone, 0), None)]
    seen = set()

    while priority_queue:
        cost, _, state, path = heapq.heappop(priority_queue)
        left, _ = state

        if not left:
            moves = []
            while path:
                move, path = path
                moves.append(move)
            return cost, moves[::-1]

        if state in seen:
            continue
        seen.add(state)

        for step_cost, new_state, move in next_states(state, everyone, times):
            heapq.heappush(priority_queue, (cost + step_cost, next(tie), new_state, (move, path)))

    print("No solution found.")
    return float("inf"), []


def read_minutes(n: int) -> list[int]:
    minutes = []
    for i in range(1, n + 1):
        while True:
            try:
                m = int(input(f"Enter minutes to cross for tourist {i}: "))
            except ValueError:
                print("Please enter a positive integer.")
                continue
            if m <= 0:
                print("Minutes must be a positive integer.")
                continue
            minutes.append(m)
            break
    return minutes


def main() -> None:
    while True:
        try:
            n = int(input("Enter the number of tourists (1-10): "))
        except ValueError:
            print("Please enter an integer between 1 and 10.")
            continue
        if 1 <= n <= 10:
            break
        print("Number of tourists must be between 1 and 10. Please enter again.")

    minutes = read_minutes(n)
    total, moves = bridge_problem(minutes)

    print("Minutes for all tourists:", minutes)
    print("Moves to cross the bridge:", moves)
    print("Shortest time to cross the bridge:", total)


if __name__ == "__main__":
    main()