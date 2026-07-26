# Unnecessary English Insertions in Chinese LLM Responses

This repository contains the experiment code and results to collect responses from four LLM providers under four prompt conditions. 

The experiment dataset contains 200 manually selected Chinese C-Eval questions. Each question is expanded into four prompt variations:

1. Baseline
2. Explicit Chinese-only instruction
3. Few-shot Chinese demonstrations
4. Penalty instruction

This produces 800 prompts and 3,200 model responses (with four models).

## Repository structure

- `data/manual_selected_dataset.jsonl`: 200 selected questions
- `data/expanded_dataset.jsonl`: 800 generated prompts
- `expand_dataset.py`: generates the four prompt variations
- `experiment.py`: runs one provider at a time
- `results/`: provider outputs and the combined 3,200-response dataset

## Run the experiment

```bash
python3 expand_dataset.py

export DEEPSEEK_API_KEY="your-key"
export QWEN_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

python3 experiment.py --provider deepseek
python3 experiment.py --provider qwen
python3 experiment.py --provider gemini
python3 experiment.py --provider openai
```

Each output row contains `variation_id`, `response`, and `token_count`. Results are appended after the corresponding JSONL files, so remove an existing provider result file before starting a fresh run.