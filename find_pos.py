from ckip_transformers.nlp import CkipPosTagger
import json
import os


# 2. 定義你在雲端硬碟中的目標資料夾路徑
# 備註：請根據你實際的資料夾名稱確認路徑是否正確
output_dir = "/content/drive/MyDrive/Colab Notebooks/Traditional-Chinese-Spelling-Error-Correction"

# 確保該資料夾存在
os.makedirs(output_dir, exist_ok=True)


def wordpos():
    # 3. 定義完整的輸出路徑
    file_path = os.path.join(output_dir, "all_words_freq_pos_ckip.json")

    # GPU
    pos_driver = CkipPosTagger(model="bert-base", device=0)

    # 所有詞
    with open("all_words.json", "r", encoding="utf-8") as f:
        words = json.load(f)

    # 原本的詞頻
    with open("words_freq_pos.json", "r", encoding="utf-8") as f:
        old_dict = json.load(f)

    # 去重
    words = sorted(set(words))

    # CKIP 一次做 POS（比一個一個快很多）
    pos_results = pos_driver([words])[0]

    result = {}

    for word, pos in zip(words, pos_results):

        if word in old_dict:
            freq = old_dict[word]["freq"]
        else:
            freq = 1

        result[word] = {
            "freq": freq,
            "pos": pos
        }


    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"完成，檔案已儲存至雲端硬碟：{file_path}，共 {len(result)} 個詞")


def charpos():

    file_path = os.path.join(output_dir, "single_chars_pos_ckip.json")

    # GPU
    pos_driver = CkipPosTagger(model="bert-base", device=0)

    # 所有詞
    with open("single_chars.json", "r", encoding="utf-8") as f:
        chars = json.load(f)
    
    # 原本的詞頻
    with open("words_freq_pos.json", "r", encoding="utf-8") as f:
        old_dict = json.load(f)

    # 去重
    chars = sorted(set(chars))

    # CKIP 一次做 POS（比一個一個快很多）
    pos_results = pos_driver([chars])[0]

    result = {}

    for char, pos in zip(chars, pos_results):

        if char in old_dict:
            freq = old_dict[char]["freq"]
        else:
            freq = 1

        result[char] = {
            "freq": freq,
            "pos": pos
        }


    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"完成，檔案已儲存至雲端硬碟：{file_path}，共 {len(result)} 個字")


charpos()