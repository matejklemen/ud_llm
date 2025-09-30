import itertools
import sys
import json
import subprocess
from collections import Counter


def get_most_common_ordering(dictionary):
    curr_most_common_freq = 0
    curr_most_common_ordering = "No ordering"
    for ordering in dictionary.keys():
        if dictionary[ordering] > curr_most_common_freq:
            curr_most_common_freq = dictionary[ordering]
            curr_most_common_ordering = ordering

    return curr_most_common_ordering

valid_result_value_combinations = {"SVO or SOV", "SVO or OVS", "SVO or OSV", "SVO or VSO",
                                   "SVO or VOS", "SOV or OVS", "SOV or OSV", "SOV or VSO", 
                                   "SOV or VOS", "OVS or OSV", "OVS or VSO", "OVS or VOS", 
                                   "OSV or VSO", "OSV or VOS", "VSO or VOS"}

filepath = sys.argv[1]
out_path = sys.argv[2]

temp_filename_1 = "81B_temp_data_(81A_result).json"
subprocess.run(["python", "81A.py", filepath, temp_filename_1])

with open(temp_filename_1, "r", encoding="utf-8") as rf_81A:
    results_81A = json.load(rf_81A)

results_81B = {}
for _opt1, _opt2 in itertools.combinations(results_81A["distribution"].keys(), r=2):
    _count_opt1 = results_81A["distribution"].get(_opt1, 0)
    _count_opt2 = results_81A["distribution"].get(_opt2, 0)

    if f"{_opt1} or {_opt2}" in valid_result_value_combinations:
        results_81B[f"{_opt1} or {_opt2}"] = _count_opt1 + _count_opt2
    elif f"{_opt2} or {_opt1}" in valid_result_value_combinations:
        results_81B[f"{_opt2} or {_opt1}"] = _count_opt2 + _count_opt1

# get most frequent ordering
most_common = get_most_common_ordering(results_81A["distribution"])

# get second most frequent ordering
dict_wo_most_common = {k: v for k, v in results_81A["distribution"].items() if k not in {most_common}}
second_most_common = get_most_common_ordering(dict_wo_most_common)

# get third most frequent ordering
dict_wo_two_most_common = {k: v for k, v in results_81A["distribution"].items() if k not in {most_common, second_most_common}}
third_most_common = get_most_common_ordering(dict_wo_two_most_common)

if most_common == "No ordering":
    final_answer = "No valid orderings"

elif second_most_common == "No ordering" or results_81A["distribution"][most_common] > results_81A["distribution"][second_most_common] * 2:
    final_answer = "Only one dominant"

elif third_most_common == "No ordering" or results_81A["distribution"][second_most_common] > results_81A["distribution"][third_most_common] * 2:
    if f"{most_common} or {second_most_common}" in valid_result_value_combinations:
        final_answer = f"{most_common} or {second_most_common}"
    else:
        final_answer = f"{second_most_common} or {most_common}"

else:
    final_answer = "No dominant order"

result = {
    "distribution": Counter(results_81B),
    "final_answer": final_answer
}

with open(out_path, "w", encoding="utf-8") as wf:
    print(result)
    json.dump(result, wf)
