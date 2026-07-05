from opencc import OpenCC
import json

cc = OpenCC("s2t")

lexicon = {}

with open("dict.txt.big", "r", encoding="utf-8") as f:

    for line in f:

        parts = line.strip().split()

        if len(parts) < 2:
            continue

        word = cc.convert(parts[0])

        try:
            freq = int(parts[1])
        except ValueError:
            continue

        # 有第三欄就讀，沒有就設為 x
        pos = parts[2] if len(parts) >= 3 else "x"

        if word not in lexicon:
            lexicon[word] = {
                "freq": freq,
                "pos": pos
            }
        else:
            # 重複詞保留最高詞頻
            if freq > lexicon[word]["freq"]:
                lexicon[word]["freq"] = freq
                lexicon[word]["pos"] = pos

print("詞數：", len(lexicon))

with open("words_freq_pos.json", "w", encoding="utf-8") as f:
    json.dump(lexicon, f, ensure_ascii=False, indent=4)