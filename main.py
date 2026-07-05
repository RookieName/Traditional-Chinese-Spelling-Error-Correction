import json
import pickle
from opencc import OpenCC
import jieba
from pycorrector import MacBertCorrector
from trie import Trie
import math
import jieba.posseg as pseg



macbert = MacBertCorrector("shibing624/macbert4csc-base-chinese")


jieba.set_dictionary('dict.txt.big') #適用於繁體語意
jieba.load_userdict('userdict.txt') #自訂庫

cc_t2s = OpenCC('t2s')
cc_s2t = OpenCC('s2t')

with open("trie.pkl", "rb") as f:
    trie_data = pickle.load(f)

trie = trie_data["trie"]
length_dict = trie_data["length_dict"]

with open("alignment.pkl", "rb") as f:
    align_data = pickle.load(f)

tw_to_cn = align_data["tw_to_cn"]
cn_to_tw = align_data["cn_to_tw"]

sorted_tw = sorted( 
    tw_to_cn.keys(),
    key=len,
    reverse=True #長詞優先
)

sorted_cn = sorted(
    cn_to_tw.keys(),
    key=len,
    reverse=True
)

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

def align_to_model(text):

    for tw in sorted_tw:
        text = text.replace(
            tw,
            tw_to_cn[tw]
        )

    return text

def back_to_taiwan(text):

    for cn in sorted_cn:
        text = text.replace(
            cn,
            cn_to_tw[cn]
        )

    return text

def get_candidate_pool(query):

    qlen = len(query)

    pool = []

    for l in range(max(1, qlen - 1), qlen + 2):
        pool.extend(length_dict.get(l, []))

    filtered = []
    for w in pool:
        overlap = len(set(query) & set(w)) / max(len(query), len(w))

        if overlap >= 0.3:
            filtered.append(w)

    return filtered

def rank(query, candidates):

    scored = []

    qlen = len(query)

    for w in candidates:

        # -------------------------
        # 1. edit distance
        # -------------------------
        d = edit_distance(query, w)

        if d > 2:
            continue

        # -------------------------
        # 2. frequency
        # -------------------------
        freq = trie.get_freq(w)

        # -------------------------
        # 3. length penalty
        # -------------------------
        len_penalty = abs(len(w) - qlen)

        # -------------------------
        # 4. final score
        # -------------------------
        score = (
            -9 * d                  # edit distance（最重要）
            -2 * len_penalty       # 長度懲罰（避免亂跳詞）
            + math.log(freq + 1)   # 詞頻（穩定性）
        )

        scored.append((score, w))

    # 排序
    scored.sort(reverse=True)

    return [w for _, w in scored[:20]]

    

def generate_candidates(query):

    pool = get_candidate_pool(query)

    result = rank(query, pool)

    return result

def preprocess(text):

    text = cc_t2s.convert(text)

    text = align_to_model(text)

    return text

def postprocess(text):

    text = cc_s2t.convert(text)

    text = back_to_taiwan(text)

    return text

def macbert_correct(text):

    result = macbert.correct(text)

    return result.get("target", text)

    """
    {'source': '我想去台北柯技大学', 'target': '我想去台北科技大学', 'errors': [('柯', '科', 5)]}
    """


def macbert_score(text):
    res = macbert.correct(text)
    return res.get("score", 0)

def macbert_rerank_with_lexicon(text):

    words = jieba.lcut(text)

    result = []

    for word in words:

        # skip
        if len(word) <= 1 or word.isdigit() or word.isascii():
            result.append(word)
            continue

        # 已在 Trie
        if trie.search(word):
            result.append(word)
            continue

        candidates = generate_candidates(word)

        if not candidates:
            result.append(word)
            continue

        best_word = word
        best_score = float("-inf")

        for c in candidates:

            tmp = result + [c] + words[len(result)+1:]
            tmp_text = "".join(tmp)
            tmp_text = cc_t2s.convert(tmp_text)  #轉成簡體句子
            print(tmp_text)

            score = macbert_score(tmp_text)

            if score > best_score:
                best_score = score
                best_word = c

        result.append(best_word)

    return "".join(result)

def lexical_correct(text):

    words = jieba.lcut(text)
    print(words)

    corrected = []

    for word in words:

        # 長度 <= 1 直接保留
        if len(word) <= 1:
            corrected.append(word)
            continue

        # 數字直接放行
        if word.isdigit():
            corrected.append(word)
            continue

        # 英文不修
        if word.isascii():
            corrected.append(word)
            continue

        # Trie 正確 → 保留
        if trie.search(word):
            corrected.append(word)
            continue

        candidates = generate_candidates(word)

        #confidence guard（避免亂修）
        if candidates and edit_distance(word, candidates[0]) <= 2:
            print(
                f"{word} -> {candidates[:5]}"
            )
            corrected.append(candidates[0])
        else:
            corrected.append(word)

    return "".join(corrected)


def pipeline(text):

   # Step 1: preprocess（只轉繁簡，不做 alignment）
    #text = preprocess(text)

    # Step 2: lexical 產生候選（不再直接修改句子）
    text = macbert_rerank_with_lexicon(text)

    # Step 3: postprocess
    text = postprocess(text)

    return text

def pipeline_old(text):

   # Step 1: preprocess
    text = preprocess(text)

    # Step 2: 
    text = macbert_correct(text)

    # Step 3: postprocess
    text = postprocess(text)

    text = lexical_correct(text)

    return text



sentence = "台積電昨天上張了100元"

result = pipeline(sentence)
result_old = pipeline_old(sentence)

print(result)
print(result_old)

"""
"昨天去了咖啡廳，點了題拉米蘇和美式啡" 舊的好
"台積電昨天上張了10點"  單一字抓不出來(新)
 
"""


"""
scored = []

    for w in candidates:
        d = edit_distance(query, w)

        # 超過 2 就不要了
        if d > 2:
            continue

        freq = trie.get_freq(w)

        score = (
            -10 * d                  # Edit Distance 權重最高
            + math.log(freq + 1)     # 詞頻輔助
        )

        scored.append((score, w))

    scored.sort(reverse=True)

    return [w for _, w in scored[:20]]

"""