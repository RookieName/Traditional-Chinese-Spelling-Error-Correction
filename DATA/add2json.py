import json
import re

def add_all_words(new_words):
    
    json_path = "all_words.json"

    with open(json_path, "r", encoding="utf-8") as f:
        words = json.load(f)

    words = sorted(set(words) | set(new_words))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)

    print(f"all_words.json：新增完成，目前 {len(words)} 個詞")


def add_alignment(new_pairs):

    json_path = "taiwan_china_vocabs.json"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 用 (taiwanese, chinese) 去重
    exist = {
        (item["taiwanese"], item["chinese"])
        for item in data
    }

    added = 0

    for item in new_pairs:

        key = (
            item["taiwanese"],
            item["chinese"]
        )

        if key not in exist:
            data.append(item)
            exist.add(key)
            added += 1

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"alignment.json：新增 {added} 筆，目前 {len(data)} 筆")


def add_word_freq(word, freq=1, pos="x"):
    with open("all_words_freq_pos_ckip.json", "r", encoding="utf-8") as f:
        lexicon = json.load(f)

    lexicon[word] = {
        "freq": freq,
        "pos": pos
    }

    with open ("all_words_freq_pos_ckip.json", "w", encoding="utf-8") as f:
        json.dump(lexicon, f, ensure_ascii=False, indent=4)

    print(f"已新增：{word}")

def add_bpmf(word,bpm):
    word = word.strip()
    bpm = bpm.strip()

    # 讀取原本資料
    with open("char2bpmf.json", "r", encoding="utf-8") as f:
        char2bpm = json.load(f)

    if len(word) != 1 or not re.search(r'[\u4e00-\u9fff]', word):
        print("請輸入單一中文字")
        return

    if word not in char2bpm:
        char2bpm[word] = []

    if bpm not in char2bpm[word]:
        char2bpm[word].append(bpm)
        print(f"新增 {word}: {bpm}")

    else:
        print("已存在")


    # 儲存
    with open("char2bpmf.json", "w", encoding="utf-8") as f:
        json.dump(
            char2bpm,
            f,
            ensure_ascii=False,
            indent=4
        )


new_words = [

]

new_alignments = [
    {
        "taiwanese": "",
        "chinese": "",
        "english": "",
        "description": ""
    }
]

# 執行更新
#add_all_words(new_words)

#add_alignment(new_alignments)

#add_word_freq("崇禮門", 1, "Nb")

