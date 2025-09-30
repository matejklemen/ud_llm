import sys
import json
import subprocess

correct_values = {
    "Postpositions": "Postp",
    "Prepositions": "Prep",
    "No adpositions": "NoAdp"
}

filepath = sys.argv[1]
out_path = sys.argv[2]

temp_filename_1 = "95A_temp_data_(83A_result).json"
temp_filename_2 = "95A_temp_data_(85A_result).json"

subprocess.run(["python", "83A.py", filepath, temp_filename_1])
subprocess.run(["python", "85A.py", filepath, temp_filename_2])

with open(temp_filename_1, "r", encoding="utf-8") as rf_83A:
    results_83A = json.load(rf_83A)

with open(temp_filename_2, "r", encoding="utf-8") as rf_85A:
    results_85A = json.load(rf_85A)

adp_result = correct_values[results_85A["final_answer"]]

final_answer = {
    "final_answer": results_83A["final_answer"] + "&" + adp_result
}

with open(out_path, "w", encoding="utf-8") as wf:
    json.dump(final_answer, wf)
