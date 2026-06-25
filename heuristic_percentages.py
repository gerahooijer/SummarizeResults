from itertools import product
from collections import defaultdict

import pandas as pd

results = defaultdict(list)

for bp, pc in list(product((True, False), (True, False))):
    algorithm_name = "CBS"
    if bp == True:
        algorithm_name += "-BP"
    if pc == True:
        algorithm_name += "-PC"


    file1 = f"heuristic_oz//summary-oz-{algorithm_name}.csv"
    file2 = f"heuristic_oz//summary-oz-{algorithm_name}-HEUR.csv"

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    print(file1)
    print(file2)

    for index in range(len(df1)):
        results[algorithm_name].append({
            "instance": df1["instance"][index],
            "heuristic score": df1["score"][index],
            "percentage": df2["score"][index] / df1["score"][index] *100,
        })

for result in results.keys():
    df = pd.DataFrame(results[result])
    df.to_csv(f"heuristic_oz/oz-percentage_score_{result}.csv", index=False)