import random
import math
import itertools
import time

# City labels A..J
CITIES = [chr(ord("A") + i) for i in range(10)]

   # Return dictionary mapping city label
def city_positions(center=(210, 210), radius=160):
    positions = {}
    cx, cy = center
    n = len(CITIES)
    for i, city in enumerate(CITIES):
        angle = 2 * math.pi * i / n
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        positions[city] = (int(x), int(y))
    return positions

def generate_distance_matrix(min_d=50, max_d=100):
    n = len(CITIES)
    m = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = random.randint(min_d, max_d)
            m[i][j] = d
            m[j][i] = d
    return m

# Return index of chosen HOME city
def pick_random_home():
    return random.randint(0, len(CITIES) - 1)

def brute_force_tsp(dist_matrix, start_idx, city_indices):
    t0 = time.time()
    best_cost = float("inf")
    best_route = None
    for perm in itertools.permutations(city_indices):
        route = [start_idx] + list(perm) + [start_idx]
        cost = 0
        for i in range(len(route) - 1):
            cost += dist_matrix[route[i]][route[i + 1]]
        if cost < best_cost:
            best_cost = cost
            best_route = route
    return best_route, best_cost, time.time() - t0

    # Greedy nearest neighbour
def nearest_neighbour_tsp(dist_matrix, start_idx, city_indices):
    t0 = time.time()
    unvisited = set(city_indices)
    route = [start_idx]
    current = start_idx
    while unvisited:
        next_city = min(unvisited, key=lambda c: dist_matrix[current][c])
        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    route.append(start_idx)
    cost = sum(dist_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))
    return route, cost, time.time() - t0

def held_karp_tsp(dist_matrix, start_idx, city_indices):

    t0 = time.time()
    n = len(city_indices)
    if n == 0:
        return [start_idx, start_idx], 0, 0.0

    idx_to_city = {i: city_indices[i] for i in range(n)}
    dp = {}  # (mask, last) - (cost, path_list_of_global_indices)

    # from start to each k
    for k in range(n):
        city = idx_to_city[k]
        dp[(1 << k, k)] = (dist_matrix[start_idx][city], [start_idx, city])

    for mask in range(1, 1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if (mask, last) not in dp:
                continue
            cost_so_far, path_so_far = dp[(mask, last)]
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                new_mask = mask | (1 << nxt)
                new_cost = cost_so_far + dist_matrix[idx_to_city[last]][idx_to_city[nxt]]
                key = (new_mask, nxt)
                candidate_path = path_so_far + [idx_to_city[nxt]]
                if key not in dp or new_cost < dp[key][0]:
                    dp[key] = (new_cost, candidate_path)

    full_mask = (1 << n) - 1
    best_cost = float("inf")
    best_path = None
    for last in range(n):
        if (full_mask, last) in dp:
            cost, path = dp[(full_mask, last)]
            total_cost = cost + dist_matrix[idx_to_city[last]][start_idx]
            if total_cost < best_cost:
                best_cost = total_cost
                best_path = path + [start_idx]

    elapsed = time.time() - t0
    return best_path, best_cost, elapsed

def _tsp_recursive_helper(dist_matrix, current, unvisited_set, start_idx):

    if not unvisited_set:
        # return path back to start
        return [current, start_idx], dist_matrix[current][start_idx]

    best_cost = float("inf")
    best_route = None
    for nxt in list(unvisited_set):
        remaining = set(unvisited_set)
        remaining.remove(nxt)
        sub_route, sub_cost = _tsp_recursive_helper(dist_matrix, nxt, remaining, start_idx)
        total_cost = dist_matrix[current][nxt] + sub_cost
        if total_cost < best_cost:
            best_cost = total_cost
            best_route = [current] + sub_route
    return best_route, best_cost

def tsp_recursive(dist_matrix, start_idx, city_indices):
 
    t0 = time.time()
    if not city_indices:
        return [start_idx, start_idx], 0, 0.0

    unvisited = set(city_indices)
    best_route, best_cost = _tsp_recursive_helper(dist_matrix, start_idx, unvisited, start_idx)
    elapsed = time.time() - t0
    return best_route, best_cost, elapsed

def run_all(dist_matrix, home_label, selected_labels):

    if dist_matrix is None:
        raise ValueError("dist_matrix is None")

    start_idx = CITIES.index(home_label)
    selected_indices = [CITIES.index(lbl) for lbl in selected_labels]

    results = {}

    # Brute force
    route_idx, cost, t = brute_force_tsp(dist_matrix, start_idx, selected_indices)
    route_lbl = [CITIES[i] for i in route_idx]
    results["Brute Force"] = {"route": route_lbl, "distance": float(cost), "time": float(t), "complexity": "O(n!)"}

    # Recursive
    route_idx, cost, t = tsp_recursive(dist_matrix, start_idx, selected_indices)
    route_lbl = [CITIES[i] for i in route_idx]
    results["Recursive TSP"] = {"route": route_lbl, "distance": float(cost), "time": float(t), "complexity": "O(n!) (recursive)"}

    # Iterative: Nearest Neighbour
    route_idx, cost, t = nearest_neighbour_tsp(dist_matrix, start_idx, selected_indices)
    route_lbl = [CITIES[i] for i in route_idx]
    results["Nearest Neighbour"] = {"route": route_lbl, "distance": float(cost), "time": float(t), "complexity": "O(n^2)"}

    # Held-Karp DP
    route_idx, cost, t = held_karp_tsp(dist_matrix, start_idx, selected_indices)
    route_lbl = [CITIES[i] for i in route_idx]
    results["Held-Karp (DP)"] = {"route": route_lbl, "distance": float(cost), "time": float(t), "complexity": "O(n^2 * 2^n)"}

    return results