import sys
import json
import subprocess
from collections import Counter


def get_combinations(dict1, dict2):
    result_dict = dict()

    for entry1 in dict1.keys():
        for entry2 in dict2.keys():
            result_dict[f"{entry1}&{entry2}"] = dict1[entry1] + dict2[entry2]

    return result_dict


filepath = sys.argv[1]
out_path = sys.argv[2]

temp_filename_1 = "97A_temp_data_(83A_result).json"
temp_filename_2 = "97A_temp_data_(87A_result).json"

subprocess.run(["python", "83A.py", filepath, temp_filename_1])
subprocess.run(["python", "87A.py", filepath, temp_filename_2])

with open(temp_filename_1, "r", encoding="utf-8") as rf_83A:
    results_83A = json.load(rf_83A)

with open(temp_filename_2, "r", encoding="utf-8") as rf_87A:
    results_87A = json.load(rf_87A)

# get the interim distributions
interim_83A = results_83A["distribution"]
interim_87A = results_87A["distribution"]

# build the combinations distribution
combinations_distrib = get_combinations(interim_83A, interim_87A)

final_answer = {
    "interim_distribution": {"83A": interim_83A, "87A": interim_87A},
    "distribution": Counter(combinations_distrib),
    "final_answer": max(combinations_distrib, key=combinations_distrib.get)
}

with open(out_path, "w", encoding="utf-8") as wf:
    print(final_answer)
    json.dump(final_answer, wf)
