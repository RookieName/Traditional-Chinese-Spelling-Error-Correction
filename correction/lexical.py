from .bpmf import word_to_bpm,generate_tone_variants,expand_bpm
import json
import pickle
import math
from trie import Trie

with open("trie.pkl", "rb") as f:
    trie_data = pickle.load(f)

trie = trie_data["trie"]
length_dict = trie_data["length_dict"]

DATA_DIR = "DATA"

with open(f"{DATA_DIR}/stop_words.json", "r", encoding="utf-8") as f:
    stop_words = set(json.load(f))

with open(f"{DATA_DIR}/single_chars.json", "r", encoding="utf-8") as f:
    single_char_set = set(json.load(f))

with open(f"{DATA_DIR}/bpmf2word.json", "r", encoding="utf-8") as f:
    bpm2word = json.load(f)

IGNORE_POS = {"Neu","FW","COLONCATEGORY","COMMACATEGORY","DASHCATEGORY","DOTCATEGORY"
                  ,"ETCCATEGORY","EXCLAMATIONCATEGORY","PARENTHESISCATEGORY","PAUSECATEGORY","PERIODCATEGORY"
                  ,"QUESTIONCATEGORY","SEMICOLONCATEGORY","SPCHANGECATEGORY","WHITESPACE"}


confusion_set = {
    "以經": "已經",
    "己經": "已經",
    "巳經": "已經",
    "因該": "應該",
    "固難": "困難",
}

def lexical_correct(words, pos_tags):

    corrected = []
    i = 0

    while i < len(words):

        word = words[i]
        pos = pos_tags[i]

        if (
            pos in IGNORE_POS
            or word in stop_words
            or word.isdigit()
            or word.isascii()
        ):
            corrected.append(word)
            i += 1
            continue

        # =================================
        # 1. 特定跨 token 錯誤
        # =================================

        if (
            i + 1 < len(words)
            and len(word) == 1
            and len(words[i + 1]) == 1
        ):

            merged = (word + words[i + 1])

            if merged in confusion_set:
                corrected.append(confusion_set[merged])
                i += 2
                continue

        # =================================
        # 2. 原本的單 token 邏輯
        # =================================


        if trie.search(word):
            corrected.append(word)
            i += 1
            continue

        candidates = generate_candidates(word,pos)

        if candidates and edit_distance(word,candidates[0]) <= 2:
            #print(f"{word} -> {candidates[:10]}")
            corrected.append(candidates[0])
        else:
            corrected.append(word)

        i += 1

    return "".join(corrected)



def edit_distance(a, b):
    m, n = len(a), len(b)

    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j

    for i in range(1, m+1):
        for j in range(1, n+1):

            cost = 0 if a[i-1] == b[j-1] else 1

            dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + cost
            )

    return dp[m][n]

def rank(query, candidates, query_pos): #詞性是分數一部分

    scored = []

    qlen = len(query)

    for w in candidates:

        if len(w) != qlen:
            continue

        # Edit Distance
        d = edit_distance(query, w)

        if d > 1:
            continue

        # 詞頻
        freq = trie.get_freq(w)

        #詞性      
        w_pos = trie.get_pos(w)
        pos_score = 0

        if query_pos and w_pos and query_pos != "x" and w_pos != "x":

            if query_pos == w_pos:
                pos_score = 1

            else:
                pos_score = -0.5

        score = (
            -1 * d
            + math.log(freq + 1)
            +pos_score
        )

        scored.append((score,w))
        

    scored.sort(reverse=True)

    return [w for _, w in scored[:10]]

def get_bpm_candidates(word):

    bpms = word_to_bpm(word)

    if not bpms:
        return []

    candidates = []

    # =================================
    # Level 1：完全注音匹配
    # =================================

    for bpm in bpms:

        if bpm in bpm2word:

            candidates.extend(
                x["word"]
                for x in bpm2word[bpm]
            )


    if candidates:

        return list(dict.fromkeys(candidates))


    # =================================
    # Level 2：先改聲調
    # =================================

    for bpm in bpms:

        variants = generate_tone_variants(bpm)

        for v in variants:

            if v in bpm2word:

                candidates.extend(
                    x["word"]
                    for x in bpm2word[v]
                )

    """
    if candidates:
        return list(dict.fromkeys(candidates))
    """

    # =================================
    # Level 3：聲母／韻母混淆
    # =================================

    for bpm in bpms:

        expanded_bpms = expand_bpm(bpm)

        for expanded in expanded_bpms:

            if expanded in bpm2word:

                candidates.extend(
                    x["word"]
                    for x in bpm2word[expanded]
                )


    return list(dict.fromkeys(candidates))

def get_candidate_pool(query):

    qlen = len(query)
    pool = []
    filtered = []


    for l in range(max(1, qlen - 1), qlen + 2):
        pool.extend(length_dict.get(l, []))

    for w in pool:

        overlap = len(set(query) & set(w)) / max(len(query), len(w))

        if overlap >= 0.3:
            filtered.append(w)

    return filtered

def generate_candidates(query, query_pos):

    # 優先使用注音候選
    if len(query) > 1:
        bpm_pool = get_bpm_candidates(query)

        if bpm_pool:
            return rank(query, bpm_pool, query_pos)

    # 其他情況或注音找不到才使用找詞頻和詞性
    candidates = get_candidate_pool(query)

    return rank(query, candidates, query_pos)
