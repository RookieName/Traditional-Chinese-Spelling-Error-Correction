from ckip_transformers import __version__
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
import json
import pickle
import glob
import os
from trie import Trie
import math

ws_driver = CkipWordSegmenter(model="bert-base", device=-1)
pos_driver = CkipPosTagger(model="bert-base", device=-1)

with open("trie.pkl", "rb") as f:
    trie_data = pickle.load(f)

trie = trie_data["trie"]
length_dict = trie_data["length_dict"]

with open("stop_words.txt", "r", encoding="utf-8") as f:
    stop_words = set(line.strip() for line in f if line.strip())

with open("single_chars.json", "r", encoding="utf-8") as f:
    single_char_set = set(json.load(f))

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

def char_level_eval(pred, gold):
    """
    return TP, FP, FN
    """

    min_len = min(len(pred), len(gold))

    tp = fp = fn = 0

    for i in range(min_len):
        if pred[i] == gold[i]:
            tp += 1
        else:
            fp += 1
            fn += 1

    # 長度補償
    if len(pred) > len(gold):
        fp += len(pred) - len(gold)
    elif len(gold) > len(pred):
        fn += len(gold) - len(pred)

    return tp, fp, fn

def compute_metrics(all_tp, all_fp, all_fn):

    accuracy = all_tp / (all_tp + all_fp + all_fn + 1e-9)
    precision = all_tp / (all_tp + all_fp + 1e-9)
    recall = all_tp / (all_tp + all_fn + 1e-9)
    f1 = 2 * precision * recall / (precision + recall + 1e-9)

    return accuracy, precision, recall, f1


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

    pool = get_candidate_pool(query)

    result = rank(query, pool, query_pos)

    return result

def rank(query, candidates, query_pos):

    scored = []

    qlen = len(query)


    for w in candidates:

        # Edit Distance
        d = edit_distance(query, w)

        if d > 2:
            continue

        # 詞頻
        freq = trie.get_freq(w)

        # 長度
        len_penalty = abs(len(w)-qlen)

        #詞性
        pos_score = 0

        w_pos = trie.get_pos(w)


        if (query_pos and w_pos and w_pos != "x"):

            if query_pos == w_pos:
                pos_score = 1

            else:
                pos_score = -0.5


        score = (
            -9 * d
            -2 * len_penalty
            + math.log(freq + 1)
            + pos_score
        )


        scored.append((score,w))


    scored.sort(reverse=True)

    return [w for _,w in scored[:10]]

def lexical_correct(words, pos_tags, ignore_words):

    corrected = []

    for word, pos in zip(words, pos_tags):

        # NER 忽略
        if word in ignore_words:
            corrected.append(word)
            continue


        if (
            word in stop_words or
            word.isdigit() or
            word.isascii()
        ):
            corrected.append(word)
            continue


        # Trie 正確
        if trie.search(word):
            corrected.append(word)
            continue


        candidates = generate_candidates(word, pos)


        if candidates and edit_distance(word, candidates[0]) <= 2:
            corrected.append(candidates[0])
        else:
            corrected.append(word)


    return "".join(corrected)


DATA_DIR = "sighan_raw/pair_data/traditional"

def main():
    sys_tp = sys_fp = sys_fn = 0

    IGNORE_POS = {"Neu"}

    error_files = glob.glob(os.path.join(DATA_DIR, "train13_error.txt"))

    for error_file in error_files:

        correct_file = error_file.replace("_error.txt", "_correct.txt")

        if not os.path.exists(correct_file):
            continue

        with open(error_file, encoding="utf-8") as f:
            error_lines = [x.strip() for x in f if x.strip()]

        with open(correct_file, encoding="utf-8") as f:
            gold_lines = [x.strip() for x in f if x.strip()]

        ws_results = ws_driver(error_lines)
        pos_results= pos_driver(error_lines)

        for words, pos, gold in zip(ws_results, pos_results, gold_lines):

            ignore_words = set()

            for word, tag in zip(words, pos):
                if tag in IGNORE_POS:
                    ignore_words.add(word)
                    
            pred = lexical_correct(words,pos,ignore_words)

            tp, fp, fn = char_level_eval(pred, gold)

            sys_tp += tp
            sys_fp += fp
            sys_fn += fn
    
    sys_metrics = compute_metrics(sys_tp, sys_fp, sys_fn)

    print("\n========== FINAL RESULT ==========")
    print("\n🟢 Your System")
    print(f"Accuracy : {sys_metrics[0]:.4f}")
    print(f"Precision: {sys_metrics[1]:.4f}")
    print(f"Recall   : {sys_metrics[2]:.4f}")
    print(f"F1       : {sys_metrics[3]:.4f}")

if __name__ == "__main__":
    main()



"""
print("原句：", sentence)
print("result : ",text)
print("-" * 50)
"""

"""
sentences = [
    "劉墉在三歲過年時，全家陷入火海，把家燒得面目全飛、體無完膚。",
    "有些人是必須歷經一場大風大浪才會改變，有的人一輩子都很好命，但是發生了想不道的事，也有可能一生都很辛苦，可是有一天他卻過著福有的生活。",
    "貝多芬是一位家喻戶曉的音樂才子，但在成為第一位音樂家之前，經過了一場風雨澈底的改變了他的命運，也使他的耳朵漸漸的聽不到了。",
    "或許我們會在挫折中有令人不同凡想的成就呢！",
    "不經一番寒轍骨，焉得梅花撲鼻香！人生中愈多逆境反而愈好，克服了愈多，成長的當然也就愈多啊！",
    "我有一千二百二十五張紙"
]
"""

"""
****train****
========== FINAL RESULT ==========

🟢 Your System
Accuracy : 0.8292
Precision: 0.9078
Recall   : 0.9055
F1       : 0.9066

****train13****(詞性同+1不同-0.5)

========== FINAL RESULT ==========

🟢 Your System
Accuracy : 0.8970
Precision: 0.9467
Recall   : 0.9447
F1       : 0.9457

"""
