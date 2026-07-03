import json
import re
from pathlib import Path
from opencc import OpenCC

cc = OpenCC("s2t")

DATA_DIR = Path("./Shameless_lexicon_data")
OUTPUT = Path("shamless_words.json")

# 保留：中文、英文、數字
pattern = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff]+")

words = set()

for txt_file in DATA_DIR.rglob("*.txt"):   # 包含子資料夾
    print(f"讀取 {txt_file.name}")

    with open(txt_file, "r", encoding="utf-8") as f:
        for line in f:

            line = line.strip()
            if not line:
                continue

            # 只取第一欄
            word = line.split()[0]

            # 簡轉繁
            word = cc.convert(word)

            # 去除特殊符號
            word = pattern.sub("", word)

            if word:
                words.add(word)

# 排序
words = sorted(words)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(words, f, ensure_ascii=False, indent=4)

print(f"\n完成！")
print(f"共 {len(words)} 個詞")
print(f"輸出：{OUTPUT}")