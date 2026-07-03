import json

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




