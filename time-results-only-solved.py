from itertools import product
import pandas as pd
import os
from glob import glob
from collections import defaultdict

output_folder = "time-results-oz"

os.makedirs(output_folder, exist_ok=True)
intermediate_results = []

results = defaultdict(list)
# Find all CSV files

input_folder = f"results-oz\\seperate"
csv_files = glob(os.path.join(input_folder, "*.csv"))
for file in csv_files:
    df = pd.read_csv(file)

    instance = 0
    for bp in [True, False]:
        for pc in [True, False]:
            for heur in [True, False]:
                for i in range(1,13):
                    if f"results-oz\\seperate\\multi_results_instance_OZ{i}({bp}, {pc}, {heur}).csv" in file:
                        instance = i
                        bp1 = bp
                        pc1 = pc
                        heur1 = heur
    if instance == 0: continue
    algorithm_name = "CBS"
    if bp1 == True:
        algorithm_name += "-BP"
    if pc1 == True:
        algorithm_name += "-PC"
    if heur1 == True:
        algorithm_name += "-HEUR"
    feasible = df["score"] != "infeasible"
    results[(instance, algorithm_name)].append(feasible)


new_results = defaultdict(list)
csv_files = glob(os.path.join(input_folder, "*.csv"))

for file in csv_files:
    df = pd.read_csv(file)
    instance = 0
    for bp in [True, False]:
        for pc in [True, False]:
            for heur in [True, False]:
                for i in range(1, 13):
                    if f"results-oz\\seperate\\multi_results_instance_OZ{i}({bp}, {pc}, {heur}).csv" in file:
                        instance = i
                        bp1 = bp
                        pc1 = pc
                        heur1 = heur
    if instance == 0: continue

    algorithm_name = "CBS"
    if bp1 == True:
        algorithm_name += "-BP"
    if pc1 == True:
        algorithm_name += "-PC"
    if heur1 == True:
        algorithm_name += "-HEUR"

    for index in range(50):
        if results[(instance, algorithm_name)][0][index] != False:
            new_results[(instance, algorithm_name)].append({
                "instance": f"{instance}-{index}",
                "algorithm": algorithm_name,
                "total_time": df["total time"][index],
                "time_in_CBS": df["time in CBS"][index]-df["time in a_star"][index],
                "time_in_astar": df["time in a_star"][index],
            })
        else:
            new_results[(instance, algorithm_name)].append({
                "instance": f"{instance}-{index}",
                "algorithm": algorithm_name,
                "total_time": None,
                "time_in_CBS": None,
                "time_in_astar": None,
            })

for (instance, algorithm_name) in new_results.keys():
    new_df = pd.DataFrame(new_results[(instance, algorithm_name)])
    new_df.to_csv(f"time-results-oz/time-instance{instance}-{algorithm_name}.csv", index=False)
