# 10-station test dataset.
from generate import generate_train_dataset, write_dataset, print_stats, verify_connected
import os

if __name__ == "__main__":
    print("Generating 10-station test dataset...")
    stations, edges = generate_train_dataset(
        num_stations=10,
        num_edges=20,
        id_range=(1, 500),
        weight_range=(1, 50),
        seed=99
    )

    out_path = os.path.join("datasets", "test", "test.txt")
    write_dataset(out_path, stations, edges)

    print_stats(stations, edges)
    connected = verify_connected(stations, edges)
    print(f"  Connected:      {'Yes' if connected else 'NO'}")
    print(f"  Written to:     {out_path}")