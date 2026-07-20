import json
from collections import defaultdict


with open("dict-concised_audio.json", "r", encoding="utf-8") as f:
    data = json.load(f)

char2bpmf = defaultdict(set)

for key in data:

    word, bpm = key.split(".",1)

    # 只處理單字
    if len(word) != 1:
        continue

    char2bpmf[word].add(bpm)

char2bpm = {
    ch:list(v)
    for ch,v in char2bpmf.items()
}

with open("char2bpmf.json","w",encoding="utf-8") as f:

    json.dump(
        char2bpm,
        f,
        ensure_ascii=False,
        indent=4
    )


print("字數:",len(char2bpm))