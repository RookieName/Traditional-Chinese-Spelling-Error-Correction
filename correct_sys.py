import json
import pickle
from opencc import OpenCC
import jieba
from pycorrector import MacBertCorrector
from trie import Trie
import math
from resources import *


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

def generate_candidates(query):

    pool = get_candidate_pool(query)

    result = rank(query, pool)

    return result

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

    
def preprocess(text):

    text = align_to_model(text)

    text = cc_t2s.convert(text)

    return text

def postprocess(text, original_text):

    text = cc_s2t.convert(text)

    text = back_to_taiwan(text)

    # ====== 保留原句關鍵詞（他/她 這種）======
    keep_tokens = {"他", "她", "你", "妳", "妳們", "你們", "他們", "她們"}

    orig_words = jieba.lcut(original_text)
    new_words = jieba.lcut(text)

    #print(orig_words)
    #print(new_words)

    fixed = []
    for o, n in zip(orig_words, new_words):
        if o in keep_tokens:
            fixed.append(o)
        else:
            fixed.append(n)

    return "".join(fixed)


def macbert_correct(text):

    result = macbert.correct(text)

    target = result.get("target", text)
    print(target)

    return target



def lexical_correct(text):

    words = jieba.lcut(text)
    print(words)

    corrected = []

    for word in words:

         #在stop words裡 or 數字 or 英文
        if (
            word in stop_words or
            word in single_char_set or
            word.isdigit() or
            word.isascii()
        ):
            corrected.append(word)
            continue
        

        # Trie 正確 → 保留
        if trie.search(word):
            corrected.append(word)
            continue

        candidates = generate_candidates(word)

        #confidence guard（避免亂修）
        if candidates and edit_distance(word, candidates[0]) <= 2:
            
            print(f"{word} -> {candidates[:5]}")
            
            corrected.append(candidates[0])
        else:
            corrected.append(word)

    return "".join(corrected)


def correct_sys(text):

    original_text = text

   # Step 1: preprocess
    text = preprocess(text)

    # Step 2: 
    text = macbert_correct(text)

    # Step 3: postprocess
    text = postprocess(text,original_text)

    text = lexical_correct(text)

    return text



