
import pandas as pd
import os
from glob import glob

output_folder = "summaries"

os.makedirs(output_folder, exist_ok=True)

for k in range(1, 13):
    # Find all CSV files
    input_folder = f"data/instance{k}"
    csv_files = glob(os.path.join(input_folder, "*.csv"))

    intermediate_results = []

    for file in csv_files:
        df = pd.read_csv(file)

        bp1 = df["bypass"][0]
        pc = df["cardial_conflicts"][0]
        heur1 = df["heuristic"][0]


        if (file != f"data/instance{k}\\multi_results_instance{k}({bp1}, {pc}, {heur1}).csv" and
                file != f"data/instance{k}\\results_instance{k}({bp1}, {pc}, {heur1}).csv"):
                print(file, "not good")


        algorithm_name = 'CBS'
        if bp1 == True:
            algorithm_name += '-BP'
        if pc == True:
            algorithm_name += '-PC'
        if heur1 == True:
            algorithm_name += '-HEUR'

        feasible_df = df[df["score"] != "infeasible"].copy()
        feasible_df["score"] = pd.to_numeric(feasible_df["score"])

        intermediate_results.append({
            "instance_set": k,
            "algorithm": algorithm_name,
            "bypass": bp1,
            "cardinal_conflicts": pc,
            "heuristic": heur1,
            "solved": len(feasible_df),
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

    int_df = pd.DataFrame(intermediate_results)
    int_df.to_csv(os.path.join(output_folder, f"{k}.csv"), index=False)