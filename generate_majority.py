import os
from collections import Counter

import pandas as pd

from constants import UD_TEST_PATHS as UD_PATHS

## Majority answers are generated according to WALS (can't rely on training distribution, not all treebanks have a training set)

feature_name = "81A"
MAJORITY_ANSWER = "SOV"

# feature_name = "82A"
# MAJORITY_ANSWER = "SV"

# feature_name = "83A"
# MAJORITY_ANSWER = "OV"

# feature_name = "84A"
# MAJORITY_ANSWER = "VOX"

# feature_name = "85A"
# MAJORITY_ANSWER = "Postpositions"

# feature_name = "86A"
# MAJORITY_ANSWER = "GenN"

# feature_name = "87A"
# MAJORITY_ANSWER = "NAdj"

# feature_name = "88A"
# MAJORITY_ANSWER = "DemN"

# feature_name = "89A"
# MAJORITY_ANSWER = "NNum"

# feature_name = "90A"
# MAJORITY_ANSWER = "NRel"

# feature_name = "94A"
# MAJORITY_ANSWER = "Adverbial subordinators which appear at the beginning of the subordinate clause"  # initial

# feature_name = "144A"
# MAJORITY_ANSWER = "Morphological negation"

# feature_name = "144B"
# MAJORITY_ANSWER = "Immediately preverbal"

problem_response_data = {
    "UD_Language": [], "WALS_Language": [],
    "Correct_value": [], "LLM_Response": [],
    "LLM_Response_postp": [], "LLM_Response_unagg": []
}

for curr_lang_ud, ud_path in UD_PATHS.items():
    problem_response_data["UD_Language"].append(curr_lang_ud)
    problem_response_data["WALS_Language"].append("/")
    problem_response_data["Correct_value"].append("/")
    problem_response_data["LLM_Response"].append(MAJORITY_ANSWER)
    problem_response_data["LLM_Response_postp"].append("")
    problem_response_data["LLM_Response_unagg"].append(str(Counter({MAJORITY_ANSWER: 1})))

problem_response_data = pd.DataFrame(problem_response_data)

experiment_dir = "majority_baseline"
os.makedirs(experiment_dir, exist_ok=True)
os.makedirs(os.path.join(experiment_dir, feature_name), exist_ok=True)
problem_response_data.to_csv(os.path.join(experiment_dir, feature_name, f"answers_{feature_name}.tsv"),
                             sep="\t", index=False)