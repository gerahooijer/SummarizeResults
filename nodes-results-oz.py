from itertools import product
import pandas as pd
import os
from glob import glob
from collections import defaultdict


intermediate_results = []
results = defaultdict(list)
# Find all CSV files

input_folder = f"10-minutes-oz\\individual"
csv_files = glob(os.path.join(input_folder, "*.csv"))
for file in csv_files:
    df = pd.read_csv(file)
    print(file)
    instance = 0
    for bp in [True, False]:
        for pc in [True, False]:
            for heur in [True, False]:
                for i in range(1, 13):
                    if f"10-minutes-oz\\individual\\10_min_multi_results_instance_OZ{i}({bp}, {pc}, {heur}).csv" in file:
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
input_folder = f"10-minutes-oz\\individual"
csv_files = glob(os.path.join(input_folder, "*.csv"))
for file in csv_files:
    df = pd.read_csv(file)

    instance = 0
    for bp in [True, False]:
        for pc in [True, False]:
            for heur in [True, False]:
                for i in range(1, 13):
                    if f"10-minutes-oz\\individual\\10_min_multi_results_instance_OZ{i}({bp}, {pc}, {heur}).csv" in file:
                        instance = i
                        bp1 = bp
                        pc1 = pc
                        heur1 = heur
    if instance == 0: continue

    algorithm_name = "CBS"

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
                "nodes_created": df["nodes_created"][index]+1,
                "nodes_bypassed": df["nodes_bypassed"][index],
                "nodes_pruned": df["nodes_pruned"][index],
                "cardinal_splits": df["cardinal_splits"][index],
                "pruned_by_cost": df["pruned_by_cost"][index],
            })
        else:
            new_results[(instance, algorithm_name)].append({
                "instance": f"{instance}-{index}",
                "algorithm": algorithm_name,
                "nodes_created": None,
                "nodes_bypassed": None,
                "nodes_pruned": None,
                "cardinal_splits": None,
                "pruned_by_cost": None,
            })

for (instance, algorithm_name) in new_results.keys():
    new_df = pd.DataFrame(new_results[(instance, algorithm_name)])
    new_df.to_csv(f"10-minutes-oz//only_solved//node-instance{instance}-{algorithm_name}.csv", index=False)
