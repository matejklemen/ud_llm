import sys
import json
import subprocess


def get_combinations(dict1, dict2):
    result_dict = dict()

    for entry1 in dict1.keys():
        for entry2 in dict2.keys():
            result_dict[f"{entry1}&{entry2}"] = dict1[entry1] + dict2[entry2]

    return result_dict


filepath = sys.argv[1]
out_path = sys.argv[2]

temp_filename_1 = "96A_temp_data_(83A_result).json"
temp_filename_2 = "96A_temp_data_(90A_result).json"

subprocess.run(["python", "83A.py", filepath, temp_filename_1])
subprocess.run(["python", "90A.py", filepath, temp_filename_2])

with open(temp_filename_1, "r", encoding="utf-8") as rf_83A:
    results_83A = json.load(rf_83A)

with open(temp_filename_2, "r", encoding="utf-8") as rf_90A:
    results_90A = json.load(rf_90A)

# get the interim distributions
interim_83A = results_83A["distribution"]
interim_90A = results_90A["distribution"]

# build the combinations distribution
combinations_distrib = get_combinations(interim_83A, interim_90A)

final_answer = {
    "interim_distribution": {"83A": interim_83A, "90A": interim_90A},
    "combinations_distribution": combinations_distrib,
    "final_answer": max(combinations_distrib, key=combinations_distrib.get)
}

with open(out_path, "w", encoding="utf-8") as wf:
    json.dump(final_answer, wf)
