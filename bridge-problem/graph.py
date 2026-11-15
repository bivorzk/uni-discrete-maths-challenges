"""A hídprobléma állapottér-gráfja NetworkX segítségével.

Egy csúcs egy ``(bal_part, lampa_oldala)`` állapotot jelöl:

* ``bal_part`` a bal oldalon tartózkodó turisták azonosítóinak halmaza;
* ``lampa_oldala`` értéke ``0`` a bal, ``1`` a jobb oldal esetén.

Egy irányított él egy szabályos átkelésnek felel meg. Az él súlya az
átkelés ideje, vagyis a csoport lassabb tagjának ideje. Így a
``networkx.shortest_path`` súlyozott változata közvetlenül megadja a
leggyorsabb megoldást.
"""

from collections import deque

import matplotlib
import networkx as nx

from main import next_states

matplotlib.use("Agg")


State = tuple[frozenset[int], int]


def build_graph(
    number_of_tourists: int, minutes_to_cross: list[int]
) -> tuple[nx.DiGraph, State, State] | None:
    """Felépíti az összes elérhető állapotot és átkelést tartalmazó gráfot.

    Az élek a ``weight`` attribútumban tartalmazzák az átkelés költségét,
    a ``move`` attribútumban pedig a megjeleníthető lépést, például
    ``("->", (1, 2))``.
    """
    if not isinstance(number_of_tourists, int) or not 1 <= number_of_tourists <= 10:
        print("Number of tourists must be between 1 and 10.")
        return None
    if not isinstance(minutes_to_cross, list):
        print("Crossing times must be provided as a list.")
        return None
    if len(minutes_to_cross) != number_of_tourists:
        print("The number of crossing times must match the tourists.")
        return None
    if any(
        not isinstance(minutes, int) or minutes <= 0
        for minutes in minutes_to_cross
    ):
        print("Minutes must be positive integers.")
        return None

    everyone = frozenset(range(1, number_of_tourists + 1))
    start: State = (everyone, 0)
    target: State = (frozenset(), 1)
    graph = nx.DiGraph()

    states_to_visit = deque([start])
    visited = {start}
    while states_to_visit:
        state = states_to_visit.popleft()
        graph.add_node(state)

        times = {tourist: minutes_to_cross[tourist - 1] for tourist in everyone}
        for cost, new_state, move in next_states(state, everyone, times):
            graph.add_edge(state, new_state, weight=cost, move=move)
            if new_state not in visited:
                visited.add(new_state)
                states_to_visit.append(new_state)

    return graph, start, target


def shortest_solution(
    number_of_tourists: int, minutes_to_cross: list[int]
) -> tuple[float, list[tuple[str, tuple[int, ...]]]]:
    """Visszaadja a leggyorsabb megoldás összidejét és lépéseit."""
    graph_data = build_graph(number_of_tourists, minutes_to_cross)
    if graph_data is None:
        return float("inf"), []
    graph, start, target = graph_data
    path = nx.shortest_path(graph, start, target, weight="weight")
    total_time = nx.path_weight(graph, path, weight="weight")
    moves = [
        graph.edges[path[index], path[index + 1]]["move"]
        for index in range(len(path) - 1)
    ]
    return total_time, moves


def format_solution(
    number_of_tourists: int, minutes_to_cross: list[int]
) -> str:
    """Táblázatos, könnyen olvasható formában jeleníti meg a megoldást."""
    total_time, moves = shortest_solution(number_of_tourists, minutes_to_cross)
    left = set(range(1, number_of_tourists + 1))
    lines = [
        "Lépés | Bal part       | Lámpa | Jobb part      | Idő",
        "------+----------------+-------+----------------+----",
    ]

    for step, (direction, group) in enumerate(moves, start=1):
        tourists = set(group)
        if direction == "->":
            left -= tourists
            lamp = "jobb"
        else:
            left |= tourists
            lamp = "bal"

        right = set(range(1, number_of_tourists + 1)) - left
        crossing_time = max(minutes_to_cross[tourist - 1] for tourist in group)
        left_text = ", ".join(map(str, sorted(left))) or "-"
        right_text = ", ".join(map(str, sorted(right))) or "-"
        group_text = ", ".join(map(str, group))
        lines.append(
            f"{step:>5} | {left_text:<14} | {lamp:<5} | "
            f"{right_text:<14} | {crossing_time:>2} "
            f"({group_text} {direction})"
        )

    lines.append(f"\nÖsszesen: {total_time} perc")
    return "\n".join(lines)


def draw_solution(
    number_of_tourists: int,
    minutes_to_cross: list[int],
    output_path: str | None = None,
) -> None:
    """Kirajzolja az állapotgráfot, a leggyorsabb utat kiemelve."""
    import matplotlib.pyplot as plt

    graph_data = build_graph(number_of_tourists, minutes_to_cross)
    if graph_data is None:
        return
    graph, start, target = graph_data
    path = nx.shortest_path(graph, start, target, weight="weight")
    path_edges = set(zip(path, path[1:]))
    positions = nx.spring_layout(graph, seed=42)

    labels = {
        state: f"Bal: {','.join(map(str, sorted(state[0])) or ['-'])}\n"
        f"Lámpa: {'bal' if state[1] == 0 else 'jobb'}"
        for state in graph
    }
    node_colors = [
        "lightgreen" if state == start else "salmon" if state == target else "lightblue"
        for state in graph
    ]
    edge_colors = [
        "crimson" if edge in path_edges else "lightgray"
        for edge in graph.edges
    ]

    plt.figure(figsize=(14, 9))
    nx.draw_networkx(
        graph,
        positions,
        labels=labels,
        node_color=node_colors,
        edge_color=edge_colors,
        node_size=1800,
        font_size=7,
        arrows=True,
        arrowsize=15,
    )
    plt.title("Hídprobléma: a leggyorsabb út az állapotgráfban")
    plt.axis("off")
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
    else:
        plt.show()
    plt.close()


if __name__ == "__main__":
    tourists = 4
    crossing_times = [1, 2, 5, 10]
    print(format_solution(tourists, crossing_times))
    draw_solution(tourists, crossing_times, "bridge_solution.png")