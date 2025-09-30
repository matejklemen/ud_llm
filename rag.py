import argparse
import importlib
import json
import os
import warnings
from collections import Counter
from typing import List

import conllu
import numpy as np
import pandas as pd
from tqdm import trange, tqdm
from transformers import pipeline, AutoTokenizer

from retrieval import random_retrieval, generic_prompt_retrieval
from constants import UD_TEST_PATHS as UD_PATHS


parser = argparse.ArgumentParser()
parser.add_argument("--experiment_dir", type=str, default="rag_v1_gpt5")
parser.add_argument("--code_dir", type=str, default="/home/matej/Documents/ud_llm/CODE_REPOSITORY/generated-code-gpt5")
parser.add_argument("--run_features", type=str, default="144B",
					help="Separate feature names with a comma (,)")

parser.add_argument("--pretrained_name_or_path", type=str, default="meta-llama/Llama-3.3-70B-Instruct")
parser.add_argument("--batch_size", type=int, default=1)
parser.add_argument("--input_repr_logic", type=str, default="conllu",  # TODO
					choices=["text", "conllu"])
parser.add_argument("--retrieval_logic", type=str, default="none",
					choices=["random", "generic_prompt", "none"])
parser.add_argument("--sample_size", type=int, default=30)
parser.add_argument("--max_new_tokens", type=int, default=64)
parser.add_argument("--random_seed", type=int, default=17)


if __name__ == "__main__":
	args = parser.parse_args()
	np.random.seed(args.random_seed)
	model_name_pretty = args.pretrained_name_or_path.split("/")[-1].lower()
	hf_access_token = "TODO"  # TODO
	os.makedirs(args.experiment_dir, exist_ok=True)

	# with open("EVALUATION_PROBLEMS.json", "r") as _f:
	# 	problem_metadata = json.load(fp=_f)
	# 	for _i in range(len(problem_metadata)):
	# 		problem_metadata[_i]["id"] = problem_metadata[_i]["id"].upper()

	features_to_run = list(map(lambda _s: _s.strip().upper(), args.run_features.split(",")))
	print(f"Running features {features_to_run}")
	# problem_metadata = [_problem for _problem in problem_metadata if _problem["id"] in features_to_run]

	# ud_languages = pd.read_csv("ud_languages.tsv", sep="\t")
	#
	# ud2wals = {}
	# for idx_lang in range(ud_languages.shape[0]):
	# 	ex = ud_languages.iloc[idx_lang]
	# 	ud_lang = ex["UD_Language"].strip()
	# 	wals_lang = ex["WALS_Language"].strip()
	#
	# 	if wals_lang != "/":
	# 		ud2wals[ud_lang] = wals_lang

	# TODO: limit to English for debugging
	# ud2wals = {"English": "English"}

	all_wals_gt = {}
	all_problem_response_data = {
		_id: {
			"UD_Language": [], "WALS_Language": [],
			"Correct_value": [], "LLM_Response": [],
			"LLM_Response_postp": [], "LLM_Response_unagg": []
		} for _id in features_to_run
	}

	for curr_lang_ud, ud_path in UD_PATHS.items():
		# ud_path = UD_PATHS[curr_lang_ud]
		print(f"------------{curr_lang_ud}------------")
		print(ud_path)

		# formatted examples = what will be given as input
		all_examples_textonly, all_examples_formatted = [], []
		with open(ud_path, "r", encoding="utf-8") as f_ud:
			for tokenlist in tqdm(conllu.parse_incr(f_ud), desc="Reading data"):
				all_examples_formatted.append(tokenlist)
				all_examples_textonly.append(tokenlist.metadata["text"])

		print(f"Total: {len(all_examples_formatted)} examples")

		for feature_name in features_to_run:
			# feature_name = _problem["id"]
			print(f"Problem {feature_name}")
			# problem_valid_answers = sorted(list(_problem["example_valid_answers"]))

			# Retrieve examples relevant for the problem
			if args.retrieval_logic == "none":
				select_indices = np.arange(len(all_examples_formatted))
			elif args.retrieval_logic == "random":
				select_indices = random_retrieval(all_examples_formatted, sample_size=args.sample_size)
			else:
				raise NotImplementedError(f"Invalid retrieval logic: '{args.retrieval_logic}'")

			examples_formatted = [all_examples_formatted[_i] for _i in select_indices]
			examples_textonly = [all_examples_textonly[_i] for _i in select_indices]

			num_selected = len(select_indices)
			num_total = len(all_examples_formatted)

			print(f"Selected {num_selected}/{num_total} relevant examples ({num_selected/max(num_total, 1)*100.0}%)!")

			problem_experiment_dir = os.path.join(args.experiment_dir, feature_name)
			os.makedirs(problem_experiment_dir, exist_ok=True)

			ud_lang_nospace = curr_lang_ud.replace(" ", "")
			lang_responses_path = os.path.join(problem_experiment_dir, ud_lang_nospace)
			os.makedirs(lang_responses_path, exist_ok=True)

			# if _problem["id"] in all_wals_gt:
			# 	# Cached ground truth to avoid constant reloading
			# 	wals2gt = all_wals_gt[_problem["id"]]
			# else:
			# 	with open(_problem["file_path"], "r") as f:
			# 		problem_data = pd.read_csv(_problem["file_path"], sep="\t")
			#
			# 	wals2gt = dict(zip(problem_data["Language"].apply(lambda _lang: _lang.strip()).tolist(),
			# 					   problem_data["Value"].apply(lambda _val: _val.strip()).tolist()))
			# 	all_wals_gt[_problem["id"]] = wals2gt

			# Skip languages that do not have a WALS ground truth label assigned
			# TODO: maybe add a flag for this
			# if curr_lang_wals not in wals2gt:
			# 	continue

			problem_response_data = all_problem_response_data[feature_name]

			responses = []
			# Load the module
			module_name = f"module_{feature_name}"
			module_path = os.path.join(args.code_dir, f"{feature_name}.py")
			spec = importlib.util.spec_from_file_location(module_name, module_path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)

			for input_ex in tqdm(all_examples_formatted, desc="Running solver"):
				try:
					ans = module.solve(input_ex)
				except Exception as e:
					ans = None
					print(f"Exn (feature {feature_name}, lang {curr_lang_ud}):\n{e}")
				responses.append(ans)

			raw_responses, cleaned_responses = [], []
			responses_to_count = []
			for _i, _response in enumerate(responses):
				raw_responses.append(str(_response))

				# If response is None, the question could not be answered for the example and should (likely?)
				# be ignored from final aggregation
				if _response is None:
					cleaned_responses.append(str(_response))
				else:
					parts = _response
					parts_filtered = []
					for _part in parts:
						_part = _part.strip()
						parts_filtered.append(_part)

					parts_filtered = list(parts_filtered)
					cleaned_responses.append(str(parts_filtered))
					responses_to_count.extend(parts_filtered)

				print(examples_textonly[_i])
				print(raw_responses[-1])
				print(cleaned_responses[-1])
				print("")

			df_agg = pd.DataFrame({
				"examples": examples_textonly,
				"LLM_Raw_response": raw_responses,
				"LLM_Response": cleaned_responses
			})
			df_agg.to_csv(os.path.join(lang_responses_path,
									   f"example_responses_{feature_name}_{ud_lang_nospace}.tsv"),
						  index=False, sep="\t")

			counter = Counter(responses_to_count)
			if len(counter.values()) > 0:
				top_resp, _count = counter.most_common(1)[0]
			else:
				top_resp, _count = "Invalid", 0

			denom = sum(counter.values())

			print(f"Aggregated response: {top_resp} ({_count} / {denom} = {100.0 * (_count/max(denom, 1)):.4f}%)")
			print(str(counter))
			problem_response_data["UD_Language"].append(curr_lang_ud)
			problem_response_data["WALS_Language"].append("/")
			problem_response_data["Correct_value"].append("/")
			problem_response_data["LLM_Response"].append(top_resp.strip())
			problem_response_data["LLM_Response_postp"].append("")
			problem_response_data["LLM_Response_unagg"].append(str(counter))

			all_problem_response_data[feature_name] = problem_response_data

	for feature_name in all_problem_response_data:
		problem_response_data = all_problem_response_data[feature_name]
		problem_response_data = pd.DataFrame(problem_response_data)
		problem_experiment_dir = os.path.join(args.experiment_dir, feature_name)

		problem_response_data.to_csv(os.path.join(problem_experiment_dir,
												  f"answers_{feature_name}.tsv"),
									 sep="\t", index=False)







