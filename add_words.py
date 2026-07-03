from lexicon_utils import add_all_words, add_alignment


new_words = [
    "好吃"
]

new_alignments = [
    {
        "taiwanese": "USB隨身碟",
        "chinese": "U盤",
        "english": "",
        "description": ""
    },
    {
        "taiwanese": "行動電源",
        "chinese": "充電寶",
        "english": "Power Bank",
        "description": ""
    }
]

# 執行更新
add_all_words(new_words)

#add_alignment(new_alignments)