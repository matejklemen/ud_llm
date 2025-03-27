import os

import pandas as pd

if __name__ == "__main__":
	# TODO: maybe I should be taking the majority label off of the entire distribution (not test set)
	file_path = "LLM_Baseline/97A/answers_97A_gpt-4o.tsv"
	df = pd.read_csv(file_path, sep="\t")
	feature_name = file_path.split(os.path.sep)[-2]

	label_counts = df["Correct_value"].value_counts()
	print("Label counts:")
	print(label_counts)
	majority_label = label_counts.index.tolist()[0]
	print(f"Majority label: {majority_label}")

	fake_llm_response = [majority_label for _ in range(df.shape[0])]
	df["LLM_Response"] = fake_llm_response
	df["LLM_Response_postp"] = fake_llm_response

	df.to_csv(f"answers_{feature_name}_majority.tsv", sep="\t", index=False)

