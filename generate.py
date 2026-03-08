import random
import os
from collections import defaultdict

def generate_train_dataset(
    num_stations=150,
    num_edges=700,
    id_range=(1, 3000),
    weight_range=(1, 100),
    seed=42
):
    
    # Generates a connected undirected weighted graph representing a train system.

    random.seed(seed)

    # Generate scattered unique station IDs
    station_ids = sorted(random.sample(range(id_range[0], id_range[1] + 1), num_stations))

    # Step 1: Build a random spanning tree to guarantee connectivity
    shuffled = station_ids[:]
    random.shuffle(shuffled)

    edges = set()
    for i in range(len(shuffled) - 1):
        a, b = shuffled[i], shuffled[i + 1]
        edge = (min(a, b), max(a, b))
        edges.add(edge)

    # Step 2: Add random edges until we reach target count
    attempts = 0
    max_attempts = num_edges * 50

    while len(edges) < num_edges and attempts < max_attempts:
        a = random.choice(station_ids)
        b = random.choice(station_ids)
        if a != b:
            edge = (min(a, b), max(a, b))
            if edge not in edges:
                edges.add(edge)
        attempts += 1

    # Step 3: Assign random weights
    edge_list = []
    for (a, b) in edges:
        w = random.randint(weight_range[0], weight_range[1])
        edge_list.append((a, b, w))

    # Shuffle so spanning tree edges aren't grouped together
    random.shuffle(edge_list)

    return station_ids, edge_list


def generate_small_test():
    """Small test dataset matching the sample in the spec."""
    stations = [1, 2, 3, 4, 5]
    edges = [
        (1, 2, 12),
        (1, 3, 8),
        (1, 4, 20),
        (1, 5, 15),
        (2, 3, 5),
        (2, 5, 25),
        (3, 4, 10),
        (4, 5, 7),
    ]
    return stations, edges


def write_dataset(filename, station_ids, edge_list):
    """Write dataset in the specified file format."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(f"{len(station_ids)} {len(edge_list)}\n")
        for a, b, w in edge_list:
            f.write(f"{a} {b} {w}\n")


def print_stats(station_ids, edge_list):
    """Print useful statistics about the generated dataset."""
    weights = [w for _, _, w in edge_list]
    
    # Calculate degree distribution
    degree = defaultdict(int)
    for a, b, _ in edge_list:
        degree[a] += 1
        degree[b] += 1
    degrees = list(degree.values())

    print(f"  Stations:       {len(station_ids)}")
    print(f"  Railroads:      {len(edge_list)}")
    print(f"  ID range:       {min(station_ids)} – {max(station_ids)}")
    print(f"  Weight range:   {min(weights)} – {max(weights)}")
    print(f"  Avg weight:     {sum(weights) / len(weights):.1f}")
    print(f"  Total weight:   {sum(weights)}")
    print(f"  Min degree:     {min(degrees)}")
    print(f"  Max degree:     {max(degrees)}")
    print(f"  Avg degree:     {sum(degrees) / len(degrees):.1f}")


def verify_connected(station_ids, edge_list):
    """BFS to verify the graph is fully connected."""
    adj = defaultdict(set)
    for a, b, _ in edge_list:
        adj[a].add(b)
        adj[b].add(a)

    visited = set()
    queue = [station_ids[0]]
    visited.add(station_ids[0])

    while queue:
        node = queue.pop(0)
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) == len(station_ids)


if __name__ == "__main__":
    # --- Main dataset ---
    print("Generating main dataset...")
    stations, edges = generate_train_dataset(
        num_stations=150,
        num_edges=700,
        id_range=(1, 3000),
        weight_range=(1, 100),
        seed=42
    )

    main_path = os.path.join("datasets", "main", "stationtostation.txt")
    write_dataset(main_path, stations, edges)

    print_stats(stations, edges)
    connected = verify_connected(stations, edges)
    print(f"  Connected:      {'Yes' if connected else 'NO — something went wrong!'}")
    print(f"  Written to:     {main_path}")
