import re


def is_noise(title):
    """
    判斷是否為不適合放入 CSC Trie 的詞
    """

    # 空字串
    if not title:
        return True

    title = title.strip()

    # 長度限制
    if len(title) < 2:
        return True

    if len(title) > 15:
        return True
    
    #開頭是數字
    if re.match(r"^[0-9]", title):
        return True
    
    #開頭是英文
    if re.match(r"^[A-Za-z]", title):
        return True

    # 空格太多（通常是句子或歌名）
    if title.count(" ") > 2:
        return True

    # 數字比例過高
    digit_count = sum(c.isdigit() for c in title)
    if digit_count / len(title) > 0.3:
        return True

    # 英文比例過高
    ascii_alpha = sum(
        c.isalpha() and ord(c) < 128
        for c in title
    )

    if ascii_alpha / len(title) > 0.8:
        return True

    # 括號過多
    if title.count("(") + title.count(")") > 2:
        return True

    # 特殊符號過多
    symbol_count = len(
        re.findall(r"[+\-*/=<>@#$%^&_~|]", title)
    )

    if symbol_count > 2:
        return True

    # 天體編號、小行星編號
    if re.match(r"^\(\d+\)", title):
        return True

    # 化學式特徵
    chemical_patterns = [
        r"\(\d",
        r"\([A-Z],[A-Z]\)",
        r"\([RSZE],[RSZE]\)",
        r"\([RSZE]\)",
        r"\d,\d",
    ]

    for p in chemical_patterns:
        if re.search(p, title):
            return True

    # 槍械口徑
    if re.match(r"^\.\d+", title):
        return True

    # 開頭是奇怪符號
    if re.match(r"^[^一-龥A-Za-z0-9]", title):
        return True
    
    #娛樂作品
    if re.search(r"\(.*專輯.*\)", title):
        return True

    if re.search(r"\(.*電影.*\)", title):
        return True

    if re.search(r"\(.*電視劇.*\)", title):
        return True

    return False


def normalize(title):
    """
    基本正規化
    """

    title = title.strip()

    # 全形空白
    title = title.replace("\u3000", " ")

    # 多空白合併
    title = re.sub(r"\s+", " ", title)

    return title


def clean_lexicon(input_file, output_file):
    lexicon = set()

    total = 0
    kept = 0
    removed = 0

    with open(input_file, "r", encoding="utf-8") as f:

        for line in f:
            total += 1

            title = normalize(line)

            if is_noise(title):
                removed += 1
                continue

            lexicon.add(title)
            kept += 1

    with open(output_file, "w", encoding="utf-8") as f:

        for word in sorted(lexicon):
            f.write(word + "\n")

    print("=" * 50)
    print("Total Titles :", total)
    print("Kept Titles  :", kept)
    print("Removed      :", removed)
    print("Final Unique :", len(lexicon))
    print("=" * 50)


if __name__ == "__main__":

    clean_lexicon(
        "wiki_titles.txt",
        "clean_titles.txt"
    )