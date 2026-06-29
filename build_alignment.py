import json
import pickle

with open("taiwan_china_vocabs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

tw_to_cn = {}
cn_to_tw = {}

for item in data:
    cn = item["chinese"].strip()
    tw = item["taiwanese"].strip()

    if cn and tw:
        tw_to_cn[tw] = cn
        cn_to_tw[cn] = tw

with open("alignment.pkl", "wb") as f:
    pickle.dump(
        {
            "tw_to_cn": tw_to_cn,
            "cn_to_tw": cn_to_tw
        },
        f
    )

print("完成")