import argparse
import os

import pandas as pd

from constants import UD_TEST_PATHS as UD_PATHS

parser = argparse.ArgumentParser()
parser.add_argument("--experiment_dir", type=str, default="gpt5_baseline_prompts",
                    help="Directory should contain raw text files 'prompt_<ID_FEATURE>.txt' with a prompt template, "
                         "where {lang_name} will be filled in")
parser.add_argument("--feature_name", type=str, default="97A")


# Creates a batch .jsonl file of OpenAI requests based on the prompt template
if __name__ == "__main__":
    args = parser.parse_args()
    experiment_dir = args.experiment_dir
    feature_name = args.feature_name
    prompt_path = os.path.join(experiment_dir, f"prompt_{feature_name}.txt")

    if not os.path.exists(prompt_path):
        raise ValueError(f"Could not find prompt template file '{prompt_path}' in the experiment dir.")

    with open(prompt_path, "r") as _f:
        prompt_content =  _f.read().strip()

    input_prompts = []
    _i = 0
    for _i, lang in enumerate(UD_PATHS):
        request_uid = f"{feature_name}-{lang}-{_i}"
        id_request = f"request-{request_uid}"
        # You are given the following input in the CONLL-U format. {query}
        input_prompts.append({
            "custom_id": id_request, "method": "POST", "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-5",
                "reasoning_effort": "high",
                "verbosity": "low",
                "messages": [
                    {"role": "user", "content": prompt_content.format(lang_name=lang)}
                ]
            }
        })

    input_prompts = pd.DataFrame.from_dict(input_prompts)
    print(input_prompts)
    input_prompts.to_json(os.path.join(experiment_dir, f"input_prompts_{feature_name}.jsonl"), orient="records", lines=True)
