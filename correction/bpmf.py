from itertools import product
import json

with open(f"DATA/char2bpmf.json", "r", encoding="utf-8") as f:
    char2bpm = json.load(f)

TONES = ["", "ˊ", "ˇ", "ˋ", "˙"]

BPM_CONFUSION = {
    "ㄓ": ["ㄓ", "ㄗ"],
    "ㄗ": ["ㄗ", "ㄓ"],
    "ㄔ": ["ㄔ", "ㄘ"],
    "ㄘ": ["ㄘ", "ㄔ"],
    "ㄕ": ["ㄕ", "ㄙ"],
    "ㄙ": ["ㄙ", "ㄕ"],
    "ㄌ": ["ㄌ", "ㄖ"],
    "ㄖ": ["ㄖ", "ㄌ"],
    "ㄣ": ["ㄣ", "ㄥ"],
    "ㄥ": ["ㄥ", "ㄣ"],
    "ㄛ": ["ㄛ", "ㄡ"],
    "ㄡ": ["ㄡ", "ㄛ"],
    "ㄢ": ["ㄢ", "ㄤ"],
    "ㄤ": ["ㄤ", "ㄢ"]
}

def remove_tone_char(syllable):

    for tone in TONES: 
        syllable = syllable.replace(tone, "")

    return syllable

def generate_tone_variants(bpm):

    syllables = bpm.split()

    results = []

    for i, syllable in enumerate(syllables):

        base = remove_tone_char(syllable)

        current_tone = ""

        for ch in syllable:

            if ch in TONES:
                current_tone = ch

        tone_variants = [
            base,
            base + "ˊ",
            base + "ˇ",
            base + "ˋ",
            "˙" + base
        ]

        for new_syllable in tone_variants:

            if new_syllable == syllable:
                continue

            new_syllables = syllables.copy()
            new_syllables[i] = new_syllable

            results.append(
                " ".join(new_syllables)
            )

    return list(dict.fromkeys(results))

def expand_bpm(bpm):

    choices = []

    for ch in bpm:

        if ch in BPM_CONFUSION:
            choices.append(BPM_CONFUSION[ch])
        else:
            choices.append([ch])

    return ["".join(x) for x in product(*choices)]

def word_to_bpm(word):

    syllables = []

    for ch in word:

        if ch not in char2bpm:
            return []

        # 只使用該字的原始讀音
        syllables.append(char2bpm[ch])

    return [" ".join(x) for x in product(*syllables)]