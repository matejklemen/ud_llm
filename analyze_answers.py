import os

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

VALID_VALUES = {
	"81A_81B": ["SOV", "SVO", "VSO", "VOS", "OVS", "OSV", "Multiple", "No dominant order"],
	"82A": ["SV", "VS", "No dominant order"],
	"83A": ["OV", "VO", "No dominant order"],
	"84A": ["VOX", "XVO", "XOV", "OXV", "OVX", "No dominant order"],
	"85A": ["Prepositions", "Postpositions", "Inpositions", "No dominant order", "No adpositions"],
	"86A": ["Genitive-Noun", "Noun-Genitive", "No dominant order"],
	"87A": ["Adjective-Noun", "Noun-Adjective", "No dominant order", "Only internally-headed relative clauses"],
	"88A": ["Demonstrative-Noun", "Noun-Demonstrative", "Demonstrative prefix", "Demonstrative suffix", "Demonstrative before and after Noun", "Mixed"],
	"89A": ["Numeral-Noun", "Noun-Numeral", "No dominant order", "Numeral only modifies verb"],
	"90B": ["Relative clause-Noun (RelN) dominant", "RelN or NRel", "RelN or internally-headed", "RelN or correlative", "RelN or double-headed"],
	"90C": ["Noun-Relative clause (NRel) dominant", "NRel or RelN", "NRel or internally-headed", "NRel or correlative"],
	"93A": ["Initial interrogative phrase", "Not initial interrogative phrase", "Mixed"],
	"94A": ["Initial subordinator word", "Final subordinator word", "Internal subordinator word", "Subordinating suffix", "Mixed"],
	"95A": ["OV and Postpositions", "OV and Prepositions", "VO and Postpositions", "VO and Prepositions", "Other"],
	"96A": ["OV and RelN", "OV and NRel", "VO and RelN", "VO and NRel", "Other"],
	"97A": ["OV and AdjN", "OV and NAdj", "VO and AdjN", "VO and NAdj", "Other"]
}

# Remap "Invalid" answers to the majority label according to WALS data (overall distribution)
INVALID_REMAP = {
	"81A_81B": "SOV",
	"82A": "SV",
	"83A": "OV",
	"84A": "VOX",
	"85A": "Postpositions",
	"86A": "Genitive-Noun",
	"87A": "Adjective-Noun",
	"88A": "Demonstrative-Noun",
	"89A": "Noun-Numeral",
	"90B": "Relative clause-Noun (RelN) dominant",
	"90C": "Noun-Relative clause (NRel) dominant",
	"93A": "Not initial interrogative phrase",
	"94A": "Initial subordinator word",
	"95A": "OV and Postpositions",
	"96A": "VO and NRel",
	"97A": "VO and NAdj"
}


def preprocess_81a_81b(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()
	if len(postp_lbl.split(",")) > 1:
		postp_lbl = "Multiple"

	if " or " in postp_lbl:
		postp_lbl = "Multiple"

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["81A_81B"]

	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_82a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()
	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["82A"]

	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_83a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()
	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["83A"]

	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_84a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()
	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["84A"]

	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_85a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()
	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["85A"]

	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_86a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()
	if postp_lbl == "genn":
		postp_lbl = "genitive-noun"

	if postp_lbl == "ngen":
		postp_lbl = "noun-genitive"

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["86A"]

	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_87a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()
	if postp_lbl == "adjn":
		postp_lbl = "Adjective-Noun"

	if postp_lbl == "nadj":
		postp_lbl = "Noun-Adjective"

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["87A"]
	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_88a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()
	if postp_lbl == "demn":
		postp_lbl = "Demonstrative-Noun"
	if postp_lbl == "ndem":
		postp_lbl = "Noun-Demonstrative"

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["88A"]
	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_89a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()
	if postp_lbl == "numn":
		postp_lbl = "Numeral-Noun"
	if postp_lbl == "nnum":
		postp_lbl = "Noun-Numeral"
	if postp_lbl == "numeral-noun":
		postp_lbl = "Numeral-Noun"

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["89A"]
	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_90b(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()
	if postp_lbl == "reln dominant":
		postp_lbl = "Relative clause-Noun (RelN) dominant".lower()

	if postp_lbl == "reln":
		postp_lbl = "Relative clause-Noun (RelN) dominant".lower()

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["90B"]
	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_90c(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()

	if postp_lbl == "nrel":
		postp_lbl = "Noun-Relative clause (NRel) dominant".lower()

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["90C"]
	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_93a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["93A"]
	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_94a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["94A"]
	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_95a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["95A"]
	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_96a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["96A"]
	postp_lbl = postp_lbl.lower()
	return postp_lbl


def preprocess_97a(initial_lbl: str):
	postp_lbl = initial_lbl.strip().lower()

	if postp_lbl == "invalid":
		postp_lbl = INVALID_REMAP["97A"]
	postp_lbl = postp_lbl.lower()
	return postp_lbl


PREPROCESS_FNS = {
	"81A_81B": preprocess_81a_81b,
	"82A": preprocess_82a,
	"83A": preprocess_83a,
	"84A": preprocess_84a,
	"85A": preprocess_85a,
	"86A": preprocess_86a,
	"87A": preprocess_87a,
	"88A": preprocess_88a,
	"89A": preprocess_89a,
	"90B": preprocess_90b,
	"90C": preprocess_90c,
	"93A": preprocess_93a,
	"94A": preprocess_94a,
	"95A": preprocess_95a,
	"96A": preprocess_96a,
	"97A": preprocess_97a
}


if __name__ == "__main__":
	file_path = "LLM_Baseline/97A/answers_97A_llama-3.3-70b-instruct.tsv"
	data = pd.read_csv(file_path, sep="\t")
	feature_name = file_path.split(os.path.sep)[-2]

	preprocess_fn = PREPROCESS_FNS[feature_name]

	valid_answers = list(map(lambda _s: _s.lower(), VALID_VALUES[feature_name]))
	val2idx = {_s: _i for _i, _s in enumerate(valid_answers)}

	encoded_correct = data["Correct_value"].apply(lambda _lbl: val2idx[preprocess_fn(_lbl)]).values
	encoded_preds = data["LLM_Response_postp"].apply(lambda _lbl: val2idx[preprocess_fn(_lbl)]).values

	acc = accuracy_score(y_true=encoded_correct, y_pred=encoded_preds)
	macro_f1 = f1_score(y_true=encoded_correct, y_pred=encoded_preds, average="macro")

	print(f"File '{file_path}'")
	print(f"Valid values: {valid_answers}")
	print(f"Accuracy/Micro F1 score: {acc:.5f}")
	print(f"Macro F1 score: {macro_f1:.5f}")
