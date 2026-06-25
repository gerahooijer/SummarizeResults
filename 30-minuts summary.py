from itertools import product
import pandas as pd
import os
from glob import glob
from collections import defaultdict

output_folder = "results-30-minutes-summary"

os.makedirs(output_folder, exist_ok=True)
intermediate_results = []

# Find all CSV files
input_folder = f"results-30-minutes"
csv_files = glob(os.path.join(input_folder, "*.csv"))

for file in csv_files:
    df = pd.read_csv(file)
    intermediate_results.append(df.iloc[0])

new_df = pd.DataFrame(intermediate_results)
new_df.to_csv(os.path.join(output_folder, "summary_results-30-minutes.csv"), index=False)