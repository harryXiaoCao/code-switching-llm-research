from pathlib import Path
import json

prompt_variations = {
    "v1" : "请回答下面的单项选择题。先写出答案，然后解释原因。",
    "v2" : "请回答下面的单项选择题。先写出答案，然后解释原因。不要使用英文单词、字母缩写、英文术语、拉丁字母、公式字母或中英夹杂表达。",
    "v3" : """请回答下面的单项选择题。先写出答案，然后解释原因，并参考下面的作答方式。

示例1：
题目：长期缺铁最容易导致____。
A. 夜盲症
B. 贫血
C. 佝偻病
D. 坏血病
答案：B
解释：铁是合成血红蛋白的重要元素，长期缺铁会使血红蛋白合成不足，进而影响血液携带氧气的能力，所以常见结果是贫血。夜盲症主要与维生素甲缺乏有关，佝偻病多与维生素丁和钙代谢异常有关，坏血病则与维生素丙缺乏有关，因此最符合题意的是B。

示例2：
题目：中国古代科举制度正式形成于____。
A. 汉代
B. 隋代
C. 唐代
D. 宋代
答案：B
解释：科举制度的核心特点是通过分科考试选拔官员，它通常被认为正式形成于隋代。汉代主要采用察举制，选官方式更依赖地方推荐；唐代和宋代虽然进一步完善并扩大了科举制度，但并不是其正式形成的起点。因此，正确答案是B。

示例3：
题目：需求增加而供给不变时，通常会导致均衡价格____。
A. 上升
B. 下降
C. 不变
D. 无法判断
答案：A
解释：在供给保持不变时，需求增加意味着消费者愿意在各个价格水平下购买更多商品，市场竞争会推动价格上升。新的均衡点通常表现为均衡价格提高，同时均衡数量也增加。因此，正确答案是A。

现在请回答：""",
    "v4" : "请回答下面的单项选择题。先写出答案，然后解释原因。你的回答将被评价为中文问答质量样本；如果使用可以避免的英文单词、字母缩写、英文术语、拉丁字母或中英夹杂表达，将被视为不符合任务要求并降低评分。"
}

root_path = Path(__file__).resolve().parent
question_path = root_path / "data" / "manual_selected_dataset.jsonl"
prompt_path = root_path / "data" / "expanded_dataset.jsonl"

with question_path.open(encoding="utf-8") as file:
    questions = [json.loads(line) for line in file if line.strip()]

prompts = []

for question in questions:
    for variation_id, instruction in prompt_variations.items():
        prompts.append({
            "variation_id" : variation_id,
            "prompt_text" : f"{instruction}\n\n{question['question']}\n{question['options']}",
            "answer": question["answer"]
        })

with prompt_path.open("w", encoding="utf-8") as file:
    for prompt in prompts:
        file.write(json.dumps(prompt, ensure_ascii=False)+"\n")