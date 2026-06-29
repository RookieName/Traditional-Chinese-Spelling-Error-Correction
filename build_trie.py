import json
import pickle
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()

            node = node.children[ch]

        node.is_word = True

    def search(self, word):
        node = self.root

        for ch in word:
            if ch not in node.children:
                return False

            node = node.children[ch]

        return node.is_word



# 讀取詞庫
with open("/Trie_data/all_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

length_dict = defaultdict(list)
trie = Trie()

for w in words:
    w = w.replace(" ", "")

    if not w:
        continue

    trie.insert(w)


    

# 儲存 Trie
with open("trie.pkl", "wb") as f:
    pickle.dump(trie,f)

print(f"Trie 建立完成，共載入 {len(words)} 個詞")