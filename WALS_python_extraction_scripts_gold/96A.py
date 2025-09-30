import sys
import json
import subprocess

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

final_answer = {
    "final_answer": results_83A["final_answer"] + "&" + results_90A["final_answer"]
}

with open(out_path, "w", encoding="utf-8") as wf:
    json.dump(final_answer, wf)
