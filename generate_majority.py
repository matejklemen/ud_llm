import argparse
import os
from collections import Counter

import pandas as pd

from constants import UD_TEST_PATHS as UD_PATHS

parser = argparse.ArgumentParser()
parser.add_argument("--feature_name", type=str, default="81A", help="Specific feature ID or 'all'")

# Majority answers are generated according to WALS (can't rely on training distribution, not all treebanks have a training set)
MAJORITY_ANSWERS_WALS = {
    "81A": "SOV",
    "81B": "SOV or SVO",
    "82A": "SV",
    "83A": "OV",
    "84A": "VOX",
    "85A": "Postpositions",
    "86A": "GenN",
    "87A": "NAdj",
    "88A": "DemN",
    "89A": "NNum",
    "90A": "NRel",
    "94A": "Adverbial subordinators which appear at the beginning of the subordinate clause",
    "95A": "OV&Postpositions",
    "96A": "VO&NRel",
    "97A": "VO&NAdj",
    "144A": "Morphological negation",
    "144B": "Immediately preverbal"
}

# Creates majority answers for a feature based on the WALS dominant value
if __name__ == "__main__":
    args = parser.parse_args()
    experiment_dir = "majority_baseline"
    os.makedirs(experiment_dir, exist_ok=True)

    features_to_run = []
    if args.feature_name == "all":
        features_to_run.extend(list(MAJORITY_ANSWERS_WALS.keys()))
    else:
        features_to_run.append(args.feature_name)

    for _feat in features_to_run:
        majority_answer = MAJORITY_ANSWERS_WALS[_feat]
        problem_response_data = {
            "UD_Language": [], "WALS_Language": [],
            "Correct_value": [], "LLM_Response": [],
            "LLM_Response_postp": [], "LLM_Response_unagg": []
        }

        for curr_lang_ud, ud_path in UD_PATHS.items():
            problem_response_data["UD_Language"].append(curr_lang_ud)
            problem_response_data["WALS_Language"].append("/")
            problem_response_data["Correct_value"].append("/")
            problem_response_data["LLM_Response"].append(majority_answer)
            problem_response_data["LLM_Response_postp"].append("")
            problem_response_data["LLM_Response_unagg"].append(str(Counter({majority_answer: 1})))

        problem_response_data = pd.DataFrame(problem_response_data)

        os.makedirs(os.path.join(experiment_dir, _feat), exist_ok=True)
        problem_response_data.to_csv(os.path.join(experiment_dir, _feat, f"answers_{_feat}.tsv"),
                                     sep="\t", index=False)