from pathlib import Path
import argparse
import json
import os
import urllib.parse
import urllib.request

# API keys
deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY")
kimi_api_key = os.environ.get("KIMI_API_KEY")
gemini_api_key = os.environ.get("GEMINI_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")

root_path = Path(__file__).resolve().parent
prompt_path = root_path / "data" / "expanded_dataset.jsonl"
results_path = root_path / "results"

parser = argparse.ArgumentParser()
parser.add_argument("--provider", required=True, choices=("deepseek", "kimi", "gemini", "openai"))
args = parser.parse_args()
provider = args.provider
result_file = results_path / f"{provider}_responses.jsonl"
if provider == "deepseek":
    api_key = deepseek_api_key
elif provider == "kimi":
    api_key = kimi_api_key
elif provider == "gemini":
    api_key = gemini_api_key
elif provider == "openai":
    api_key = openai_api_key

with prompt_path.open(encoding="utf-8") as file:
    prompts = [json.loads(line) for line in file if line.strip()]

completed_results = []

for i in range(len(completed_results), len(prompts)):
    prompt = prompts[i]
    for j in range(4):
        try:
            headers = {"Content-Type" : "application/json"}
            if provider == "deepseek":
                url = "https://api.deepseek.com/chat/completions"
                headers["Authorization"] = f"Bearer {api_key}"
                payload = {
                    "model" : "deepseek-v4-flash",
                    "messages" : [{"role" : "user", "content" : prompt["prompt_text"]}],
                    "max_tokens" : 800,
                    "temperature" : 0.0,
                    "stream" : False,
                    "thinking" : {"type": "disabled"}
                }
            elif provider == "kimi":
                url = "https://api.moonshot.cn/v1/chat/completions"
                headers["Authorization"] = f"Bearer {api_key}"
                payload = {
                    "model" : "kimi-k2.6",
                    "messages" : [{"role" : "user", "content" : prompt["prompt_text"]}],
                    "max_completion_tokens" : 800,
                    "temperature" : 0.6,
                    "stream" : False,
                    "thinking" : {"type": "disabled"}
                }
            elif provider == "gemini":
                model_name = urllib.parse.quote("models/gemini-2.5-flash", safe="/")
                url = (
                    f"https://generativelanguage.googleapis.com/v1beta/"
                    f"{model_name}:generateContent?key={urllib.parse.quote(api_key)}"
                )
                payload = {
                    "contents" : [{"parts" : [{"text" : prompt["prompt_text"]}]}],
                    "generationConfig" : {
                        "maxOutputTokens" : 800,
                        "temperature" : 0.0,
                        "thinkingConfig" : {
                            "thinkingBudget" : 0,
                            "includeThoughts" : False
                        }
                    }
                }
            elif provider == "openai":
                url = "https://api.openai.com/v1/responses"
                headers["Authorization"] = f"Bearer {api_key}"
                payload = {
                    "model": "gpt-5.4-mini",
                    "input": prompt["prompt_text"],
                    "max_output_tokens": 800,
                    "temperature": 0.0,
                    "reasoning": {"effort": "none"}
                }
            request = urllib.request.Request(
                url,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(request, timeout=90) as api_response:
                data = json.loads(api_response.read().decode("utf-8"))

            if provider == "deepseek" or provider == "kimi":
                response_text = data["choices"][0]["message"]["content"].strip()
                token_count = data["usage"]["completion_tokens"]
            elif provider == "gemini":
                response_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                token_count = data["usageMetadata"]["candidatesTokenCount"]
            else:
                response_parts = []
                for output in data["output"]:
                    for content in output.get("content", []):
                        if "text" in content:
                            response_parts.append(content["text"])
                response_text = "\n".join(response_parts).strip()
                token_count = data["usage"]["output_tokens"]

            if not response_text:
                raise RuntimeError("The API returned an empty response")
            break

        except Exception as e:
            if j == 3:
                raise RuntimeError(f"Failed at prompt {i + 1}: {e}") from e
            print(e)
    result = {
        "variation_id" : prompt["variation_id"],
        "response" : response_text,
        "token_count" : token_count
    }
    with result_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(result, ensure_ascii=False)+"\n")