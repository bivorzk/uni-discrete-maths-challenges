import heapq

def get_bank(left, side, everyone):
    """Az a part, ahol a lámpa van (csak onnan indulhat átkelés)."""
    return left if side == 0 else everyone - left


def crossing_groups(bank):
    """Minden lehetséges csoport: 1 vagy 2 ember a lámpás parton."""
    singles = [(a,) for a in bank]
    pairs = [(a, b) for a in bank for b in bank if a < b]
    return singles + pairs


def crossing_time(group, times):
    """Az átkelés ideje a leglassabb csoporttag ideje."""
    return max(times[p] for p in group)


def apply_move(left, side, group):
    """Az új bal part: balra->jobbra kikerülnek, jobbra->balra visszakerülnek."""
    g = frozenset(group)
    return left - g if side == 0 else left | g


def next_states(state, everyone, times):
    """Az állapotból elérhető (költség, új állapot, lépés) hármasok."""
    left, side = state
    arrow = "->" if side == 0 else "<-"
    for group in crossing_groups(get_bank(left, side, everyone)):
        new_state = (apply_move(left, side, group), 1 - side)
        yield crossing_time(group, times), new_state, (arrow, group)


def bridge_problem(number_of_tourists, minutes_to_cross):
    times = {i + 1: minutes_to_cross[i] for i in range(number_of_tourists)}
    everyone = frozenset(times)
    start = (everyone, 0)  # mindenki balra, a lámpa is balra

    pq = [(0, start, [])]
    seen = set()

    while pq:
        cost, state, moves = heapq.heappop(pq)
        left, _ = state

        if not left:
            return cost, moves
        if state in seen:
            continue
        seen.add(state)

        for step_cost, new_state, move in next_states(state, everyone, times):
            heapq.heappush(pq, (cost + step_cost, new_state, moves + [move]))

    return float("inf"), []

def number_of_tourists(nums):
    if nums <= 0 or nums > 10:
        raise ValueError("Number of tourists must be between 1 and 10.")
    return nums

def minutes_to_cross(nums):
    # Validate the tourist count first
    num_tourists = number_of_tourists(nums)
    
    tourist_minutes = []
    
    # Collect minutes for each tourist inside this function
    for i in range(1, num_tourists + 1):
        mins = int(input(f"Enter minutes to cross for tourist {i}: "))
        if mins <= 0:
            raise ValueError("Minutes must be a positive integer.")
        tourist_minutes.append(mins)
        
    return tourist_minutes

def main():
    nums = int(input("Enter the number of tourists (1-10): "))
    while nums <= 0 or nums > 10:
        nums = int(input("Number of tourists must be between 1 and 10. Please enter again: "))
    
    times = minutes_to_cross(nums)
    
    print("Minutes for all tourists:", times)
    print("Shortest time to cross the bridge:", bridge_problem(nums, times)[0])

if __name__ == "__main__":
    main()