import sys
import json
import subprocess

filepath = sys.argv[1]
out_path = sys.argv[2]

temp_filename_1 = "90C_temp_data_(90A_result).json"
subprocess.run(["python", "90A.py", filepath, temp_filename_1])

with open(temp_filename_1, "r", encoding="utf-8") as rf_90A:
    results_90A = json.load(rf_90A)

interim_distrib = results_90A["distribution"]
reln_freq = interim_distrib["RelN"]
nrel_freq = interim_distrib["NRel"]

if nrel_freq > reln_freq * 2:
    final_answer = "NRel dominant"
else:
    final_answer = "NRel not dominant"

result = {
    "interim_distribution": interim_distrib,
    "final_answer": final_answer
}

with open(out_path, "w", encoding="utf-8") as wf:
    json.dump(result, wf)
