from itertools import product
import pandas as pd
import os
from glob import glob
from collections import defaultdict

output_folder = "heuristic_oz"

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
                for k in range(1,13):
                    if f"results-oz\\seperate\\multi_results_instance_OZ{k}({bp}, {pc}, {heur}).csv" == file:
                        instance = k
                        bp1 = bp
                        pc1 = pc
                        heur1 = heur
                        break
    if instance == 0:
        break

    algorithm_name = "CBS"
    if bp1 == True:
        algorithm_name += "-BP"
    if pc1 == True:
        algorithm_name += "-PC"
    if heur1 == True:
        algorithm_name += "-HEUR"
    feasible = df["score"] != "infeasible"

    results[(instance, algorithm_name)].append(feasible)

for (instance, algorithm) in results.keys():
    for (instance2, algorithm2) in results.keys():
        if instance == instance2 and algorithm == f"{algorithm2}-HEUR":

            for index, value in enumerate(results[(instance, algorithm)][0]):
                if results[(instance, algorithm2)][0][index] != value:
                    results[(instance, algorithm2)][0][index] = False
                    results[(instance, algorithm)][0][index] = False

print(results[(9, "CBS-HEUR")])

csv_files = glob(os.path.join(input_folder, "*.csv"))
new_results = defaultdict(list)

for file in csv_files:
    df = pd.read_csv(file)
    instance = 0
    for bp in [True, False]:
        for pc in [True, False]:
            for heur in [True, False]:
                for k in range(1,13):
                    if f"results-oz\\seperate\\multi_results_instance_OZ{k}({bp}, {pc}, {heur}).csv" == file:
                        bp1 = bp
                        pc1 = pc
                        heur1 = heur
                        instance = k
                        break
    if instance == 0:
        break

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
                "score": df["score"][index]
            })
        else:
            new_results[(instance, algorithm_name)].append({
                "instance": f"{instance}-{index}",
                "algorithm": algorithm_name,
                "score": "not_solved"
            })

for (instance, algorithm_name) in new_results.keys():
    new_df = pd.DataFrame(new_results[(instance, algorithm_name)])
    new_df.to_csv(f"heuristic_oz/instance{instance}-{algorithm_name}.csv", index=False)
