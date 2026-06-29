import json
import pickle
from transformers import AutoTokenizer, AutoModelForMaskedLM
from opencc import OpenCC
import Jieba


with open("trie.pkl", "rb") as f:
    trie = pickle.load(f)

print(trie.search(""))


with open("alignment.pkl", "rb") as f:
    data = pickle.load(f)

tw_to_cn = data["tw_to_cn"]
cn_to_tw = data["cn_to_tw"]

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

model_path = "./models/chinese-macbert-base"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForMaskedLM.from_pretrained(model_path)