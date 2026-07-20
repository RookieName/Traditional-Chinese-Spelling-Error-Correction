from itertools import product
import json
from collections import defaultdict


with open("all_words_freq_pos_ckip.json", "r",encoding="utf-8") as f:
    lexicon = json.load(f)

with open("char2bpmf.json", "r", encoding="utf-8") as f:
    char2bpm = json.load(f)

def normalize_bpm(bpm):

    result = []
    current = ""

    tones_end = {"ˊ", "ˇ", "ˋ"}

    for ch in bpm:

        # 全形空白 = 音節分隔
        if ch == "　":
            if current:
                result.append(current)
                current = ""
            continue


        # 輕聲 = 新音節開始
        if ch == "˙":

            if current:
                result.append(current)

            current = "˙"
            continue


        current += ch


        # 二三四聲代表目前音節結束
        if ch in tones_end:

            result.append(current)
            current = ""


    if current:
        result.append(current)


    return " ".join(result)



bpm2word=defaultdict(list)
added = 0
miss = set()

#第二次用單個字的注音拼成詞的注音
for word, info in lexicon.items():

    if(word.isdigit() or word.isascii()):
        continue

    bpms = []
    ok = True

    for ch in word:

        if ch not in char2bpm:
            miss.add(ch)
            ok = False
            break

        bpms.append(char2bpm[ch][0])

    if not ok:
        continue


    bpm = " ".join(bpms)

    bpm2word[bpm].append({
        "word": word,
        "freq": info["freq"],
        "pos": info["pos"]
    })



# 詞頻排序
for bpm in bpm2word:

    bpm2word[bpm].sort(
        key=lambda x:x["freq"],
        reverse=True
    )


with open("bpmf2word.json","w", encoding="utf-8") as f:

    json.dump(
        bpm2word,
        f,
        ensure_ascii=False,
        indent=4
    )

with open("missing_bpmf.json", "w", encoding="utf-8") as f:
    json.dump(
        sorted(list(miss)),
        f,
        ensure_ascii=False,
        indent=4
    )


print("注音數量:",len(bpm2word))