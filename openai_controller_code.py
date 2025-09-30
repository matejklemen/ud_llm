if __name__ == "__main__":
    from openai import OpenAI

    input_prompts_file = "gpt5_baseline/input_prompts_144B.jsonl"
    batch_task_description = "144B GPT5 baseline"

    API_KEY="TODO"  # Change this to your API key
    client = OpenAI(api_key=API_KEY)

    # Create input_prompts_{feature}.jsonl by running generate_baseline.py
    batch_input_file = client.files.create(
        file=open(input_prompts_file, "rb"),
        purpose="batch"
    )
    print(batch_input_file)

    batch_input_file_id = batch_input_file.id
    client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": batch_task_description
        }
    )


