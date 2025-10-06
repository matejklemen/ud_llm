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

temp_filename_1 = "144C_temp_data_(81A_result).json"
temp_filename_2 = "144C_temp_data_(144A_result).json"

subprocess.run(["python", "81A.py", filepath, temp_filename_1])
subprocess.run(["python", "144A.py", filepath, temp_filename_2])

with open(temp_filename_1, "r", encoding="utf-8") as rf_81A:
    results_81A = json.load(rf_81A)

with open(temp_filename_2, "r", encoding="utf-8") as rf_144A:
    results_144A = json.load(rf_144A)

# get the interim distributions
interim_81A = results_81A["distribution"]
interim_144A = results_144A["distribution"]

# build the combinations distribution
combinations_distrib = get_combinations(interim_81A, interim_144A)

if results_144A["final_answer"] == "Morphological negation":
    change = "No difference"
else:
    positive_ordering = results_81A["final_answer"]
    negative_ordering = results_144A["final_answer"].replace("Neg", "")
    if positive_ordering == negative_ordering:
        change = "No difference"
    else:
        change = f"{positive_ordering}, but {results_144A['final_answer']}"

final_answer = {
    "interim_distribution": {"81A": interim_81A, "144A": interim_144A},
    "distribution": Counter(combinations_distrib),
    "final_answer": change
}

with open(out_path, "w", encoding="utf-8") as wf:
    print(final_answer)
    json.dump(final_answer, wf)
