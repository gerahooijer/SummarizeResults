
import pandas as pd
import os
from glob import glob
from collections import defaultdict

output_folder = "results"

os.makedirs(output_folder, exist_ok=True)
intermediate_results = []

results = defaultdict(list)
for k in range(1, 13):
    # Find all CSV files
    input_folder = f"data/instance{k}"
    csv_files = glob(os.path.join(input_folder, "*.csv"))


    for file in csv_files:
        df = pd.read_csv(file)

        bp1 = df["bypass"][0]
        pc = df["cardial_conflicts"][0]
        heur1 = df["heuristic"][0]


        if (file != f"data/instance{k}\\multi_results_instance{k}({bp1}, {pc}, {heur1}).csv" and
                file != f"data/instance{k}\\results_instance{k}({bp1}, {pc}, {heur1}).csv"):
                print(file, "not good")


        algorithm_name = "CBS"
        if bp1 == True:
            algorithm_name += "-BP"
        if pc == True:
            algorithm_name += "-PC"
        if heur1 == True:
            algorithm_name += "-HEUR"

        feasible_df = df[df["score"] != "infeasible"].copy()
        feasible_df["score"] = pd.to_numeric(feasible_df["score"])

        results[algorithm_name].append({
            "instance_set": k,
            "algorithm": algorithm_name,
            "bypass": bp1,
            "cardinal_conflicts": pc,
            "heuristic": heur1,
            "solved": len(feasible_df)/0.5,
            "avg_score": feasible_df["score"].mean() if len(feasible_df) else None,
            "avg_total_time": df["total time"].mean(),
            "avg_time_in_CBS": df["time in CBS"].mean(),
            "avg_time_in_astar": df["time in a_star"].mean(),
            "avg_treesize": df["treesize"].mean(),
            "avg_nodes_created": df["nodes_created"].mean(),
            "avg_nodes_bypassed": df["nodes_bypassed"].mean(),
            "avg_nodes_pruned": df["nodes_pruned"].mean(),
            "avg_cardinal_splits": df["cardinal_splits"].mean(),
            "avg_pruned_by_cost": df["pruned_by_cost"].mean()
        })
print(results.keys())
for index, i in enumerate(results.keys()):
    print(i)
    int_df = pd.DataFrame(results[i])
    int_df.to_csv(os.path.join(output_folder, f"kb-{i}.csv"), index=False)