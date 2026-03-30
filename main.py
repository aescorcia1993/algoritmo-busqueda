from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import heapq
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple


@dataclass(frozen=True)
class Edge:
    to: str
    line: str
    time: int


Graph = Dict[str, List[Edge]]


@dataclass
class SearchConfig:
    blocked_stations: Set[str]
    blocked_lines: Set[str]
    congested_stations: Set[str]
    avoid_congested: bool
    transfer_penalty: int
    max_total_time: Optional[int] = None


Rule = Callable[[str, Edge, SearchConfig], bool]


def station_is_open(_: str, edge: Edge, config: SearchConfig) -> bool:
    return edge.to not in config.blocked_stations


def line_is_open(_: str, edge: Edge, config: SearchConfig) -> bool:
    return edge.line not in config.blocked_lines


def congestion_rule(_: str, edge: Edge, config: SearchConfig) -> bool:
    if not config.avoid_congested:
        return True
    return edge.to not in config.congested_stations


RULES: Sequence[Rule] = (station_is_open, line_is_open, congestion_rule)


def allowed_neighbors(
    graph: Graph,
    station: str,
    config: SearchConfig,
) -> Iterable[Edge]:
    for edge in graph.get(station, []):
        if all(rule(station, edge, config) for rule in RULES):
            yield edge


def reconstruct(
    prev: Dict[Tuple[str, Optional[str]], Tuple[Tuple[str, Optional[str]], Edge]],
    end_state: Tuple[str, Optional[str]],
) -> Tuple[List[str], List[Edge]]:
    stations: List[str] = [end_state[0]]
    edges: List[Edge] = []
    state = end_state
    while state in prev:
        parent, edge = prev[state]
        edges.append(edge)
        stations.append(parent[0])
        state = parent
    stations.reverse()
    edges.reverse()
    return stations, edges


def ucs_best_route(
    graph: Graph,
    start: str,
    goal: str,
    config: SearchConfig,
) -> Optional[Tuple[List[str], List[Edge], int]]:
    # State includes current station and current line to model transfer penalty.
    start_state = (start, None)
    pq: List[Tuple[int, str, Optional[str]]] = [(0, start, None)]
    best_cost: Dict[Tuple[str, Optional[str]], int] = {start_state: 0}
    prev: Dict[Tuple[str, Optional[str]], Tuple[Tuple[str, Optional[str]], Edge]] = {}

    while pq:
        cost, station, current_line = heapq.heappop(pq)
        state = (station, current_line)
        if cost != best_cost.get(state):
            continue

        if station == goal:
            if config.max_total_time is not None and cost > config.max_total_time:
                return None
            stations, edges = reconstruct(prev, state)
            return stations, edges, cost

        for edge in allowed_neighbors(graph, station, config):
            transfer_cost = 0
            if current_line is not None and current_line != edge.line:
                transfer_cost = config.transfer_penalty
            next_cost = cost + edge.time + transfer_cost
            next_state = (edge.to, edge.line)
            if next_cost < best_cost.get(next_state, float("inf")):
                best_cost[next_state] = next_cost
                prev[next_state] = (state, edge)
                heapq.heappush(pq, (next_cost, edge.to, edge.line))

    return None


def bfs_route(
    graph: Graph,
    start: str,
    goal: str,
    config: SearchConfig,
) -> Optional[List[str]]:
    queue = deque([start])
    visited = {start}
    parent: Dict[str, str] = {}

    while queue:
        node = queue.popleft()
        if node == goal:
            route = [goal]
            while route[-1] != start:
                route.append(parent[route[-1]])
            route.reverse()
            return route

        for edge in allowed_neighbors(graph, node, config):
            nxt = edge.to
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = node
                queue.append(nxt)
    return None


def sample_graph() -> Graph:
    # Undirected graph represented with explicit two-way edges.
    return {
        "PortalNorte": [Edge("Calle100", "L1", 5), Edge("Suba", "L2", 8)],
        "Calle100": [
            Edge("PortalNorte", "L1", 5),
            Edge("Heroes", "L1", 6),
            Edge("Suba", "L3", 7),
        ],
        "Heroes": [Edge("Calle100", "L1", 6), Edge("Centro", "L1", 6)],
        "Centro": [
            Edge("Heroes", "L1", 6),
            Edge("Sur", "L1", 7),
            Edge("Suba", "L3", 8),
        ],
        "Suba": [
            Edge("PortalNorte", "L2", 8),
            Edge("Calle100", "L3", 7),
            Edge("Centro", "L3", 8),
            Edge("Sur", "L2", 10),
        ],
        "Sur": [Edge("Centro", "L1", 7), Edge("Suba", "L2", 10)],
    }


def describe_result(stations: List[str], edges: List[Edge], total_cost: int) -> None:
    print("Ruta UCS:", " -> ".join(stations))
    print(f"Costo total (minutos + penalizacion): {total_cost}")

    if not edges:
        print("Sin desplazamientos.")
        return

    transfers = 0
    current_line = edges[0].line
    segments = [f"{stations[0]} --[{edges[0].line}/{edges[0].time}m]--> {stations[1]}"]

    for i in range(1, len(edges)):
        edge = edges[i]
        if edge.line != current_line:
            transfers += 1
            current_line = edge.line
        segments.append(f"{stations[i]} --[{edge.line}/{edge.time}m]--> {stations[i+1]}")

    print("Detalle:")
    for segment in segments:
        print("  ", segment)
    print(f"Transbordos: {transfers}")


def run_case(title: str, config: SearchConfig) -> None:
    print("=" * 70)
    print(title)
    print("=" * 70)

    graph = sample_graph()
    start, goal = "PortalNorte", "Sur"

    ucs = ucs_best_route(graph, start, goal, config)
    if ucs is None:
        print("UCS: No existe ruta valida para las reglas actuales.")
    else:
        stations, edges, total_cost = ucs
        describe_result(stations, edges, total_cost)

    bfs = bfs_route(graph, start, goal, config)
    if bfs is None:
        print("BFS: No existe ruta valida para las reglas actuales.")
    else:
        print("Ruta BFS (minimo numero de estaciones):", " -> ".join(bfs))


def main() -> None:
    base = SearchConfig(
        blocked_stations=set(),
        blocked_lines=set(),
        congested_stations={"Heroes"},
        avoid_congested=False,
        transfer_penalty=4,
        max_total_time=None,
    )

    run_case("Caso 1: Operacion normal", base)

    case2 = SearchConfig(
        blocked_stations={"Centro"},
        blocked_lines=set(),
        congested_stations={"Heroes"},
        avoid_congested=False,
        transfer_penalty=4,
        max_total_time=None,
    )
    run_case("Caso 2: Estacion Centro cerrada", case2)

    case3 = SearchConfig(
        blocked_stations=set(),
        blocked_lines={"L1"},
        congested_stations={"Heroes", "Suba"},
        avoid_congested=True,
        transfer_penalty=4,
        max_total_time=30,
    )
    run_case("Caso 3: Evitar congestion y linea L1 cerrada", case3)


if __name__ == "__main__":
    main()
