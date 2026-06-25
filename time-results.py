
import pandas as pd
import os
from glob import glob

output_folder = f"results-oz"

os.makedirs(output_folder, exist_ok=True)

# Find all CSV files
input_folder = f"results"
csv_files = glob(os.path.join(input_folder, "*.csv"))


for file in csv_files:
    print(file)
    df = pd.read_csv(file)
    time_results = []
    algorithm= df["algorithm"][0]
    result_df = pd.DataFrame({
        "instance_set": df["instance_set"],
        "algorithm": df["algorithm"],
        "total_time": df["avg_total_time"],
        "time_in_HL": df["avg_time_in_CBS"] - df["avg_time_in_astar"],
        "time_in_LL": df["avg_time_in_astar"],
        "time_in_HL_vs_LL":
            (df["avg_time_in_CBS"] - df["avg_time_in_astar"])/df["avg_time_in_astar"] ,
    })

    df = pd.DataFrame(time_results)
    result_df.to_csv(os.path.join(output_folder, f"time-{algorithm}-oz.csv"), index=False)