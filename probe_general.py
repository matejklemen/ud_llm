import argparse

import pandas as pd
import torch
from transformers import pipeline

problem_metadata = [
	{
		"id": "81A_81B",
		"prompt": "What is the order of subject and verb in the {lang_wals} language? The options are one or more of Subject-object-verb (SOV); Subject-verb-object (SVO); Verb-subject-object (VSO); Verb-object-subject (VOS); Object-verb-subject (OVS); Object-subject-verb (OSV); Lacking a dominant word order (No dominant order). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/81A_81B/wals.tsv"
	},
	{
		"id": "82A",
		"prompt": "What is the order of subject and verb in the {lang_wals} language? The options are Subject precedes verb (SV); Subject follows verb (VS); Both orders with neither order dominant (No dominant order). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/82A/wals.tsv"
	},
	{
		"id": "83A",
		"prompt": "What is the order of object and verb in the {lang_wals} language? The options are Object precedes verb (OV); Object follows verb (VO); Both orders with neither order dominant (No dominant order). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/83A/wals.tsv"
	},
	{
		"id": "84A",
		"prompt": "What is the order of object, oblique and verb in the {lang_wals} language? The options are Verb-object-oblique (VOX); Oblique-verb-object (XVO); Oblique-object-verb (XOV); Object-oblique-verb (OXV); Object-verb-oblique (OVX); More than one order with none dominant (No dominant order). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/84A/wals.tsv"
	},
	{
		"id": "85A",
		"prompt": "What is the order of adposition and noun phrase in the {lang_wals} language? The options are Postpositions; Prepositions; Inpositions; More than one adposition type with none dominant (No dominant order); No adpositions. Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/85A/wals.tsv"
	},
	{
		"id": "86A",
		"prompt": "What is the order of genitive and noun in the {lang_wals} language? The options are Genitive-noun (GenN); Noun-genitive (NGen); Both orders occur with neither order dominant (No dominant order). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/86A/wals.tsv"
	},
	{
		"id": "87A",
		"prompt": "What is the order of adjective and noun in the {lang_wals} language? The options are Modifying adjective precedes noun (AdjN); Modifying adjective follows noun (NAdj); Both orders of noun and modifying adjective occur, with neither dominant (No dominant order); Adjectives do not modify nouns, occurring as predicates in internally headed relative clauses (Only internally-headed relative clauses). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/87A/wals.tsv"
	},
	{
		"id": "88A",
		"prompt": "What is the order of demonstrative and noun in the {lang_wals} language? The options are Demonstrative word precedes noun (DemN); Demonstrative word follows noun (NDem); Demonstrative prefix on noun (Demonstrative prefix); Demonstrative suffix on noun (Demonstrative suffix); Demonstrative simultaneously before and after noun (Demonstrative before and after Noun); Two or more of above types with none dominant (No dominant order). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/88A/wals.tsv"
	},
	{
		"id": "89A",
		"prompt": "What is the order of numeral and noun in the {lang_wals} language? The options are Numeral precedes noun (NumN); Numeral follows noun (NNum); Both orders of numeral and noun with neither order dominant (No dominant order); Numeral only modifies verb. Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/89A/wals.tsv"
	},
	{
		"id": "90B",
		"prompt": "How are prenominal relative clauses positioned relative to the noun in the {lang_wals} language? The options are Relative clause-Noun (RelN) dominant; RelN or NRel; RelN or internally-headed; RelN or correlative; RelN or double-headed. Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/90B/wals.tsv"
	},
	{
		"id": "90C",
		"prompt": "How does the language use postnominal relative clauses, and where do they appear in relation to the noun in the {lang_wals} language? The options are Noun-Relative clause (NRel) dominant; NRel or RelN; NRel or internally-headed; NRel or correlative. Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/90C/wals.tsv"
	},
	{
		"id": "93A",
		"prompt": "Where are interrogative phrases positioned in content questions in the {lang_wals} language? The options are Interrogative phrases obligatorily initial (Initial interrogative phrase); Interrogative phrases not obligatorily initial (Not initial interrogative phrase); Mixed, some interrogative phrases obligatorily initial, some not (Mixed). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/93A/wals.tsv"
	},
	{
		"id": "94A",
		"prompt": "What is the order of adverbial subordinator and clause in the {lang_wals} language? The options are Adverbial subordinators which are separate words and which appear at the beginning of the subordinate clause (Initial subordinator word); Adverbial subordinators which are separate words and which appear at the end of the subordinate clause (Final subordinator word); Clause-internal adverbial subordinators (Internal subordinator word); Suffixal adverbial subordinators (Subordinating suffix); More than one type of adverbial subordinators with none dominant (Mixed). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/94A/wals.tsv"
	},
	{
		"id": "95A",
		"prompt": "What is the relationship between the order of object and verb and the order of adposition and noun phrase in the {lang_wals} language? The options are Object-verb and postpositional (OV and Postpositions); Object-verb and prepositional (OV and Prepositions); Verb-object and postpositional (VO and Postpositions); Verb-object and prepositional (VO and Prepositions); Languages not falling into one of the preceding four types (Other). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/95A/wals.tsv"
	},
	{
		"id": "96A",
		"prompt": "What is the relationship between the order of object and verb and the order of relative clause and noun in the {lang_wals} language? The options are Object-verb and relative clause-noun (OV and RelN); Object-verb and noun-relative clause (OV and NRel); Verb-object and relative clause-noun (VO and RelN); Verb-object and noun-relative clause (VO and NRel); Languages not falling into one of the preceding four types (Other). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/96A/wals.tsv"
	},
	{
		"id": "97A",
		"prompt": "What is the relationship between the order of object and verb and the order of adjective and noun in the {lang_wals} language? The options are Object-verb and adjective-noun (OV and AdjN); Object-verb and noun-adjective (OV and NAdj); Verb-object and adjective-noun (VO and AdjN); Verb-object and noun-adjective (VO and NAdj); Languages not falling into one of the preceding four types (Other). Answer concisely in one sentence. Do not provide an explanation.",
		"max_new_tokens": 32,
		"file_path": "WALS_data/97A/wals.tsv"
	}
]

parser = argparse.ArgumentParser()
parser.add_argument("--model_handle", type=str, default="meta-llama/Llama-3.2-1B-Instruct")
parser.add_argument("--model_name_pretty", type=str, default="llama-3.2-1b-instruct")
parser.add_argument("--hf_access_token", type=str, default=None)  # TODO: change me to your HuggingFace access token

if __name__ == "__main__":
	args = parser.parse_args()
	model_name = args.model_handle
	model_name_pretty = args.model_name_pretty
	pipeline = pipeline(
		"text-generation",
		model=model_name,
		token=args.hf_access_token,
		batch_size=4,
		device_map="auto",
		torch_dtype=torch.bfloat16
	)
	# pipeline.tokenizer.pad_token_id = pipeline.model.config.eos_token_id  # EuroLLM
	pipeline.tokenizer.pad_token_id = pipeline.model.config.eos_token_id[0]  # LLama3.x
	pipeline.tokenizer.padding_side = "left"

	ud_languages = pd.read_csv("ud_languages.tsv", sep="\t")

	ud2wals = {}
	for idx_lang in range(ud_languages.shape[0]):
		ex = ud_languages.iloc[idx_lang]
		ud_lang = ex["UD_Language"].strip()
		wals_lang = ex["WALS_Language"].strip()

		if wals_lang != "/":
			ud2wals[ud_lang] = wals_lang

	for _problem in problem_metadata:
		print(f"Problem {_problem['id']}:")
		if "file_path" not in _problem:
			continue

		with open(_problem["file_path"], "r") as f:
			problem_data = pd.read_csv(_problem["file_path"], sep="\t")

		wals2gt = dict(zip(problem_data["Language"].apply(lambda _lang: _lang.strip()).tolist(),
						   problem_data["Value"].apply(lambda _order: _order.strip()).tolist()))

		input_prompts = []
		lang_pairs = []
		for curr_lang_ud, curr_lang_wals in ud2wals.items():
			# Skip languages that do not have a WALS ground truth label assigned
			if curr_lang_wals not in wals2gt:
				continue

			input_prompts.append([{"role": "user", "content": _problem["prompt"].format(lang_wals=curr_lang_wals)}])
			lang_pairs.append((curr_lang_ud, curr_lang_wals))

		responses = pipeline(input_prompts, max_new_tokens=_problem["max_new_tokens"])

		problem_response_data = {
			"UD_Language": [], "WALS_Language": [],
			"Correct_value": [], "LLM_Response": [],
			"LLM_Response_postp": []
		}
		for _i, _response in enumerate(responses):
			_lang_ud, _lang_wals = lang_pairs[_i]
			_model_answer = _response[0]["generated_text"][-1]["content"]
			print(f"{_lang_ud} (WALS: {_lang_wals})")
			print(_model_answer)

			problem_response_data["UD_Language"].append(_lang_ud)
			problem_response_data["WALS_Language"].append(_lang_wals)
			problem_response_data["Correct_value"].append(wals2gt[_lang_wals])
			problem_response_data["LLM_Response"].append(_model_answer.strip())
			problem_response_data["LLM_Response_postp"].append("")

		problem_response_data = pd.DataFrame(problem_response_data)
		problem_response_data.to_csv(f"answers_{_problem['id']}_{model_name_pretty}.tsv", sep="\t", index=False)


























