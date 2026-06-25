
import pandas as pd
import os
from glob import glob
from collections import defaultdict

output_folder = "10-minutes-oz\\algorithms"

os.makedirs(output_folder, exist_ok=True)
intermediate_results = []

results = defaultdict(list)
# Find all CSV files
input_folder = f"10-minutes-oz"
csv_files = glob(os.path.join(input_folder, "*.csv"))

import multiprocessing as mp

for file in csv_files:
    df = pd.read_csv(file)

    instance = 0

    for i in range(1, 13):
        if f"10-minutes-oz\\10_min_multi_results_instance_OZ{i}.csv" == file:
            instance = i
    if instance == 0: continue
    print(file)
    for index, algorithm in enumerate(df["algorithm"]):
        algorithm_name = algorithm
        print(algorithm_name)

        row = df.iloc[index]

        results[algorithm_name].append(row)

for index, i in enumerate(results.keys()):
    print(i)
    int_df = pd.DataFrame(results[i])
    int_df = int_df.sort_values("instance_set")
    int_df.to_csv(os.path.join(output_folder, f"10-min-oz-{i}.csv"), index=False)