import sys
import json
import subprocess

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
    "final_answer": change
}

with open(out_path, "w", encoding="utf-8") as wf:
    json.dump(final_answer, wf)
