import warnings


def postprocess_qwen3(raw_response: str):
    # Qwen3 models first output their thinking process inside <think></think>, then the final output
    _idx_eot = raw_response.find("</think>")

    postp_response = raw_response
    if _idx_eot == -1:
        warnings.warn("Could not find </think> tag in model response. Perhaps the number of max new tokens is set too low. "
                      "Returning unprocessed response. Response:\n"
                      f"'{raw_response}'")
    else:
        postp_response = raw_response[_idx_eot + len("</think>"):].strip()

    return postp_response