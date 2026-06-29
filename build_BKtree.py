import json
import pickle


class BKNode:
    def __init__(self, word):
        self.word = word
        self.children = {}  # distance → node


class BKTree:
    def __init__(self):
        self.root = None

    def insert(self, word):
        if self.root is None:
            self.root = BKNode(word)
            return

        node = self.root

        while True:
            d = edit_distance(word, node.word)

            if d in node.children:
                node = node.children[d]
            else:
                node.children[d] = BKNode(word)
                break

    def search(self, word, max_dist):
        result = []

        def dfs(node):
            if node is None:
                return

            d = edit_distance(word, node.word)

            if d <= max_dist:
                result.append((node.word, d))

            for dist in node.children:
                if d - max_dist <= dist <= d + max_dist:
                    dfs(node.children[dist])

        dfs(self.root)
        return result


def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return dp[m][n]




with open("/Trie_data/all_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

bk = BKTree()

for w in words:
    w = w.replace(" ", "")
    
    if not w:
        continue

    bk.insert(w)

# 儲存 BKtree
with open("BKtree.pkl", "wb") as f:
    pickle.dump(bk,f)

print("BK-tree 建立完成")