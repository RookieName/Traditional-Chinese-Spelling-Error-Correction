import json
import glob
import os

# data 資料夾
data_dir = "data"

# 找所有 = 開頭的 json
files = glob.glob(os.path.join(data_dir, "=*.json"))

print(f"找到 {len(files)} 個檔案")

words = set()
single_chars = set()

for file in files:
    print("讀取:", file)

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for word in data:

        if not isinstance(word, str):
            continue

        word = word.strip()

        if word == "":
            continue

        if len(word) == 1:
            single_chars.add(word)
        else:
            words.add(word)

# 排序
words = sorted(words)
single_chars = sorted(single_chars)

# 輸出到 Trie_data 根目錄
with open("all_words.json", "w", encoding="utf-8") as f:
    json.dump(words, f, ensure_ascii=False, indent=2)

with open("single_chars.json", "w", encoding="utf-8") as f:
    json.dump(single_chars, f, ensure_ascii=False, indent=2)

print()
print("===== 完成 =====")
print("詞數量:", len(words))
print("單字數量:", len(single_chars))