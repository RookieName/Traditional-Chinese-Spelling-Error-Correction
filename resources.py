import jieba
import json
import pickle
from opencc import OpenCC
from pycorrector import MacBertCorrector

macbert = MacBertCorrector("shibing624/macbert4csc-base-chinese")

# -----------------------
# jieba
# -----------------------
jieba.set_dictionary('dict.txt.big')
jieba.load_userdict('userdict.txt')

# -----------------------
# OpenCC
# -----------------------
cc_t2s = OpenCC('t2s')
cc_s2t = OpenCC('s2t')

# -----------------------
# Trie + length_dict
# -----------------------
with open("trie.pkl", "rb") as f:
    trie_data = pickle.load(f)

trie = trie_data["trie"]
length_dict = trie_data["length_dict"]

# -----------------------
# alignment
# -----------------------
with open("alignment.pkl", "rb") as f:
    align_data = pickle.load(f)

tw_to_cn = align_data["tw_to_cn"]
cn_to_tw = align_data["cn_to_tw"]

sorted_tw = sorted(tw_to_cn.keys(), key=len, reverse=True)
sorted_cn = sorted(cn_to_tw.keys(), key=len, reverse=True)

# -----------------------
# stop words
# -----------------------
with open("stop_words.txt", "r", encoding="utf-8") as f:
    stop_words = set(line.strip() for line in f if line.strip())

# -----------------------
# single chars
# -----------------------
with open("single_chars.json", "r", encoding="utf-8") as f:
    single_char_set = set(json.load(f))