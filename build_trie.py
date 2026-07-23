from trie import Trie
import json
import pickle
from collections import defaultdict

DATA_DIR = "DATA"

# 詞庫+詞頻+詞性
with open(f"{DATA_DIR}/all_words_freq_pos_ckip.json", "r", encoding="utf-8") as f:
    lexicon = json.load(f)

# 字庫+詞頻+詞性
with open(f"{DATA_DIR}/single_chars_pos_ckip.json", "r", encoding="utf-8") as f:
    chars = json.load(f)

length_dict = defaultdict(list)
trie = Trie()

for w, info in lexicon.items():

    w = w.replace(" ", "")

    if not w:
        continue

    freq = info.get("freq", 1)
    pos = info.get("pos", "x")

    trie.insert(
        w,
        freq=freq,
        pos=pos
    )

    length_dict[len(w)].append(w)

for w, info in chars.items():

    w = w.replace(" ", "")

    if not w:
        continue

    freq = info.get("freq", 1)
    pos = info.get("pos", "x")

    trie.insert(
        w,
        freq=freq,
        pos=pos
    )

    length_dict[len(w)].append(w)

# 儲存 Trie
with open("trie.pkl", "wb") as f:
    pickle.dump({
        "trie": trie,
        "length_dict": length_dict
    }, f)

print(f"Trie 建立完成，共載入 {len(lexicon)} 個詞")
print(f"Trie 建立完成，共載入 {len(chars)} 個字")