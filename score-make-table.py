
from itertools import product
import pandas as pd
import os
from glob import glob
from collections import defaultdict

from main import algorithm_name

input_folder = f"heuristic_summaries"
csv_files = glob(os.path.join(input_folder, "*.csv"))

table = defaultdict(list)

for file in csv_files:
    df = pd.read_csv(file)
    algorithm_name = df["algorithm"].iloc[0]
    table[algorithm_name].append(
        