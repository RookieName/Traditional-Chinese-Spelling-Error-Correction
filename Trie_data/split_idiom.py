import json
import re

input_file = "=成語.json"

output_words = []

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

for phrase in data:

    if not isinstance(phrase, str):
        continue

    phrase = phrase.strip()

    if not phrase:
        continue

    # 原句保留
    output_words.append(phrase)

    # 拆分（用中文標點）
    parts = re.split(r"[，、；：！？]", phrase)

    clean_parts = []

    for p in parts:
        p = p.strip()
        if p:
            clean_parts.append(p)
            output_words.append(p)


# 去重（避免重複）
output_words = sorted(set(output_words))

# 輸出：拆完詞庫
with open("=成語_拆分後.json", "w", encoding="utf-8") as f:
    json.dump(output_words, f, ensure_ascii=False, indent=2)


print("完成！")
print("原詞 + 拆分詞數量:", len(output_words))