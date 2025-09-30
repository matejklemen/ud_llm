import os

import pandas as pd

experiment_dir = "gpt5_baseline"
feature_name = "144B"
file_path = f"outputs_{feature_name}.jsonl"

in_path = os.path.join(experiment_dir, file_path)
data = pd.read_json(file_path, orient="records", lines=True)

## Finding missing answers in the OpenAI response .jsonl file
# print(data)
# print(data.columns)
# for _i, _val in enumerate(data["custom_id"].tolist()):
#     _i_id = int(_val.split("-")[-1])
#
#     if _i != _i_id:
#         print(f"{_i} vs {_i_id}")
# exit(0)

problem_response_data = {
    "UD_Language": [], "WALS_Language": [],
    "Correct_value": [], "LLM_Response": [],
    "LLM_Response_postp": [], "LLM_Response_unagg": []
}

for idx_ex in range(data.shape[0]):
    ex = data.iloc[idx_ex]
    _id = ex["custom_id"]
    _ud_lang = _id.split("-")[-2]

    _model_response = ex["response"]["body"]["choices"][0]["message"]["content"]
    _parts = _model_response.split("\n")
    _majority = _parts[0]
    _distrib = eval(_parts[-1])
    # Workaround: in the prompts, we ask for a distribution, but in our evaluation code,
    #   we expect counts which we normalize back into a distribution
    for _k in _distrib.keys():
        _distrib[_k] = int(_distrib[_k] * 1000)

    problem_response_data["UD_Language"].append(_ud_lang)
    problem_response_data["WALS_Language"].append("/")
    problem_response_data["Correct_value"].append("/")
    problem_response_data["LLM_Response"].append(_majority)
    problem_response_data["LLM_Response_postp"].append("")
    problem_response_data["LLM_Response_unagg"].append(str(_distrib))


problem_response_data = pd.DataFrame(problem_response_data)
target_dir = os.path.join(experiment_dir, feature_name)
os.makedirs(target_dir, exist_ok=True)
problem_response_data.to_csv(os.path.join(target_dir, f"answers_{feature_name}.tsv"),
                             sep="\t", index=False)

