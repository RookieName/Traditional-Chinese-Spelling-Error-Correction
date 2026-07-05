class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
        self.freq = 0
        self.pos = "x"

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, freq=1, pos="x"):
        node = self.root

        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]

        node.is_word = True
        # 如果同一個詞插入多次，保留最高詞頻
        node.freq = max(node.freq, freq)
        node.pos = pos

    def search(self, word):
        node = self.root

        for ch in word:
            if ch not in node.children:
                return False

            node = node.children[ch]

        return node.is_word
    
    def get_freq(self, word):
        node = self.root

        for ch in word:
            if ch not in node.children:
                return 0

            node = node.children[ch]

        if node.is_word:
            return node.freq

        return 0

    def get_pos(self, word):
        node = self.root

        for ch in word:
            if ch not in node.children:
                return 0

            node = node.children[ch]

        if node.is_word:
            return node.pos

        return 0