from trie import Trie
import json
import pickle
from collections import defaultdict

# 詞庫
with open("all_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

# 詞頻+詞性
with open("words_freq_pos.json", "r", encoding="utf-8") as f:
    lexicon = json.load(f)

length_dict = defaultdict(list)
trie = Trie()

for w in words:

    w = w.replace(" ", "")

    if not w:
        continue

    info = lexicon.get(w)

    if info:
        freq = info["freq"]
        pos = info["pos"]
    else:
        freq = 1
        pos = "x"

    trie.insert(w, freq=freq, pos=pos)
    length_dict[len(w)].append(w)



with open("trie.pkl", "wb") as f:
    pickle.dump({
        "trie": trie,
        "length_dict": length_dict
    }, f)

print(f"Trie 建立完成，共載入 {len(words)} 個詞")