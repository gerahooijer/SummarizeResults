from itertools import product
import pandas as pd
import os
from glob import glob
from collections import defaultdict

new_results = defaultdict(list)

input_folder = f"time-results-kb"
csv_files = glob(os.path.join(input_folder, "*.csv"))

for file in csv_files:
    df = pd.read_csv(file)
    algorithm_name =df["algorithm"][0]
    print(file)
    instance = 0
    for k in range(1,13):
        if file == f"time-results-kb\\time-instance{k}-{algorithm_name}.csv":
            print(file)
            instance = k
            break

    if instance == 0:
        break
    print("instance", instance, "with algorithm", algorithm_name)
    new_results[algorithm_name].append({
        "instance": instance,
        "algorithm": algorithm_name,
        "avg_time_in_CBS": df["total_time"].mean(),
        "avg_time_in_astar": df["time_in_astar"].mean(),
        "time_astar_over_CBS": df["time_in_astar"].mean()/(df["total_time"]-df["time_in_astar"]).mean()*100,
    })

for algorithm in new_results.keys():
    print(algorithm)
    new_df = pd.DataFrame(new_results[algorithm])
    new_df = new_df.sort_values("instance")
    new_df.to_csv(f"time-results-summaries/summary-kb-{algorithm}.csv", index=False)
