from itertools import product
import pandas as pd
import os
from glob import glob
from collections import defaultdict

new_results = defaultdict(list)

input_folder = f"heuristic_oz"
csv_files = glob(os.path.join(input_folder, "*.csv"))

for file in csv_files:
    df = pd.read_csv(file)
    feasible_df = df[df["score"] != "not_solved"]
    feasible_df["score"] = pd.to_numeric(feasible_df["score"])
    algorithm_name =df["algorithm"][0]

    instance = 0
    for k in range(1,13):
        if file == f"heuristic_oz\\instance{k}-{algorithm_name}.csv":
            print(file)
            instance = k
            break

    if instance == 0:
        break
    print("instance", instance, "with algorithm", algorithm_name)
    new_results[algorithm_name].append({
        "instance": instance,
        "algorithm": algorithm_name,
        "score" : feasible_df["score"].mean() if len(feasible_df) else None,
    })

for algorithm in new_results.keys():
    print(algorithm)
    new_df = pd.DataFrame(new_results[algorithm])
    new_df = new_df.sort_values("instance")
    new_df.to_csv(f"heuristic_oz/summary-oz-{algorithm}.csv", index=False)
