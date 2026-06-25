from itertools import product
import pandas as pd
import os
from glob import glob
from collections import defaultdict

new_results = defaultdict(list)

input_folder = f"node-results-kb"
csv_files = glob(os.path.join(input_folder, "*.csv"))

for file in csv_files:
    df = pd.read_csv(file)
    algorithm_name =df["algorithm"][0]
    instance = 0
    for k in range(1,13):
        if file == f"node-results-kb\\node-instance{k}-{algorithm_name}.csv":
            print(file)
            instance = k
            break

    if instance == 0:
        break

    new_results[algorithm_name].append({
        "instance": instance,
        "algorithm": algorithm_name,
        "avg_nodes_created": df["nodes_created"].mean(),
        "avg_nodes_bypassed": df["nodes_bypassed"].mean(),
        "avg_nodes_pruned": df["nodes_pruned"].mean(),
        "avg_cardinal_splits": df["cardinal_splits"].mean(),
        "avg_pruned_by_cost": df["pruned_by_cost"].mean(),
    })

for algorithm in new_results.keys():
    print(algorithm)
    new_df = pd.DataFrame(new_results[algorithm])
    new_df = new_df.sort_values("instance")
    new_df.to_csv(f"node-results-summaries\\node-summary-kb-{algorithm}.csv", index=False)
