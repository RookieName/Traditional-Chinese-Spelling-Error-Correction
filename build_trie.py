from trie import Trie
import json
import pickle
from collections import defaultdict

# 讀取詞庫
with open("all_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

length_dict = defaultdict(list)
trie = Trie()

for w in words:
    w = w.replace(" ", "")

    if not w:
        continue

    trie.insert(w)
    length_dict[len(w)].append(w)


    

# 儲存 Trie
with open("trie.pkl", "wb") as f:
    pickle.dump({
        "trie": trie,
        "length_dict": length_dict
    },f)

print(f"Trie 建立完成，共載入 {len(words)} 個詞")