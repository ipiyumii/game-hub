import itertools
import time

# Complexity notes:
# - brute_force_tsp : O(n!) time, O(n) extra memory for route
# - nearest_neighbour_tsp : O(n^2) time (for naive implementation), O(n) memory
# - held_karp_tsp (dynamic programming) : O(n^2 * 2^n) time, O(n * 2^n) memory

def brute_force_tsp(dist_matrix, start_idx, city_indices):
    """Brute force by permutation. city_indices list of target indices (ints).
    Returns (route_indices_list, total_distance, elapsed_time)."""
    t0 = time.time()
    best_cost = float("inf")
    best_route = None
    for perm in itertools.permutations(city_indices):
        route = [start_idx] + list(perm) + [start_idx]
        cost = 0
        for i in range(len(route) - 1):
            cost += dist_matrix[route[i]][route[i+1]]
        if cost < best_cost:
            best_cost = cost
            best_route = route
    return best_route, best_cost, time.time() - t0

def nearest_neighbour_tsp(dist_matrix, start_idx, city_indices):
#    Greedy nearest neighbour
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
    cost = sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
    return route, cost, time.time() - t0

def held_karp_tsp(dist_matrix, start_idx, city_indices):
   
    t0 = time.time()
    # Map city_indices to 0..n-1 for DP bitmasking
    n = len(city_indices)
    if n == 0:
        return [start_idx, start_idx], 0, 0.0
    # index -> original global index
    idx_to_city = {i: city_indices[i] for i in range(n)}
    # distances between the selected cities and start
    # dp[(mask, last_index)] = (cost, path(list of global indices))
    dp = {}
    # base cases: paths starting at start_idx going to each k
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
                if key not in dp or new_cost < dp[key][0]:
                    dp[key] = (new_cost, path_so_far + [idx_to_city[nxt]])

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