import json
import glob
from collections import Counter

files = glob.glob("=*.json")

print(f"找到 {len(files)} 個檔案\n")

total_stats = {}

for file in files:
    print(f"處理檔案: {file}")

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    seen = set()
    cleaned = []
    counter = Counter(data)

    duplicate_words = []

    # 不處理空白，只做 strip + 去重
    for word in data:
        if not isinstance(word, str):
            continue

        word = word.strip()

        if word == "":
            continue

        if word in seen:
            duplicate_words.append(word)
            continue

        seen.add(word)
        cleaned.append(word)

    # 排序（統一結果）
    cleaned = sorted(cleaned)

    # 覆蓋原檔
    with open(file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    # 統計資訊
    stats = {
        "original_count": len(data),
        "cleaned_count": len(cleaned),
        "removed_duplicates": len(duplicate_words)
    }

    total_stats[file] = stats

    # log 輸出
    print("  原始數量:", stats["original_count"])
    print("  清理後數量:", stats["cleaned_count"])
    print("  移除重複:", stats["removed_duplicates"])

    if duplicate_words:
        print("  重複詞範例(最多10個):", duplicate_words[:10])

    print("-" * 40)
