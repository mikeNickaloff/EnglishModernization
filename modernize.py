#!/usr/bin/env python3
"""
modernize.py

Transforms English text into a simplified spelling using CMU pronunciations,
mirroring the logic used in eng_to_us.html. Unknown words are left unchanged.
"""

import argparse
import re
import sys
from typing import Dict, List, Tuple


PHONEME_MAP: Dict[str, str] = {
    "AA": "a", "AE": "a", "AH": "a", "AO": "o", "AW": "ow", "IY": "y",
    "B": "b", "CH": "ch", "D": "d", "DH": "th", "EH": "e", "ER": "ur",
    "EY": "ai", "F": "f", "G": "g", "HH": "h", "IH": "i", "IY": "ee",
    "JH": "j", "K": "k", "L": "l", "M": "m", "N": "n", "NG": "ng",
    "OW": "o", "OY": "oy", "P": "p", "R": "r", "S": "s", "SH": "sh",
    "T": "t", "TH": "th", "UH": "oo", "UW": "oo", "V": "v", "W": "w",
    "Y": "y", "Z": "s", "ZH": "zh",
}

VOWELS = {
    "AA","AE","AH","AO","AW","AY","EH","ER","EY","IH","IY","OH","OY","UH","UW",
}

FORCED_OVERRIDE = {
    "the": "tha",
}

FALLBACK_LEXICON: Dict[str, List[str]] = {
    "weight": ["W", "EY", "T"],
    "sacks": ["S", "AE", "K", "S"],
    "thorough": ["TH", "ER", "OW"],
    "through": ["TH", "R", "UW"],
    "neighborhood": ["N", "EY", "B", "ER", "HH", "UH", "D"],
    "transmission": ["T", "R", "AE", "N", "S", "M", "IH", "SH", "AH", "N"],
    "brought": ["B", "R", "AO", "T"],
    "gray": ["G", "R", "EY"],
    "color": ["K", "AH", "L", "ER"],
    "attacker": ["AH", "T", "AE", "K", "ER"],
}

COMPLEX_PATTERN = re.compile(r"(ough|eigh|igh|our|gue|que|eau|sion|tion|ph)")


def base_phoneme(p: str) -> str:
    return re.sub(r"[0-9]", "", p or "")


def is_vowel(p: str) -> bool:
    return base_phoneme(p) in VOWELS


def phonemes_to_simplified(phonemes: List[str]) -> Tuple[str, List[str]]:
    segments: List[Tuple[str, str]] = []  # (text, type)
    notes: List[str] = []
    add_final_e = False

    def push(text: str, seg_type: str, note: str = None):
        segments.append((text, seg_type))
        if note:
            notes.append(note)

    i = 0
    while i < len(phonemes):
        curr = base_phoneme(phonemes[i])
        nxt = base_phoneme(phonemes[i + 1]) if i + 1 < len(phonemes) else ""
        prv = base_phoneme(phonemes[i - 1]) if i > 0 else ""

        if curr == "K" and nxt == "S":
            push("x", "cons", "k+s → x")
            i += 2
            continue

        if curr == "EY":
            if i == len(phonemes) - 2 and not is_vowel(nxt):
                push("a", "vowel", "final EY → a·e")
                add_final_e = True
            else:
                push("ay", "vowel")
            i += 1
            continue

        if curr == "ER":
            if not nxt or not is_vowel(nxt) or nxt == "HH":
                push("a", "vowel", "er → a (unrhotic)")
            else:
                push("ur", "vowel")
            i += 1
            continue

        if curr == "AH" and nxt == "N" and i == len(phonemes) - 2:
            push("i", "vowel", "final AH N → in")
            i += 1
            continue

        if curr == "AH":
            if nxt == "N":
                if prv in ("K", "G"):
                    push("o", "vowel", "AH between stop+N → o")
                elif prv == "SH" or is_vowel(prv):
                    push("e", "vowel", "AH before N → e")
                else:
                    push("u", "vowel", "AH before N → u")
                i += 1
                continue
            if i == 0:
                push("u", "vowel", "initial AH → u")
                i += 1
                continue
            if prv in ("K", "G", "P", "B") and not is_vowel(nxt):
                push("o", "vowel", "AH after stop → o")
                i += 1
                continue
            if prv and not is_vowel(prv):
                push("u", "vowel", "AH unstressed → u")
                i += 1
                continue

        if curr == "AA":
            if prv == "R":
                push("o", "vowel", "AA after R → o")
                i += 1
                continue

        if curr == "UH":
            push("oo", "vowel")
            i += 1
            continue

        mapped = PHONEME_MAP.get(curr, curr.lower())
        push(mapped, "vowel" if is_vowel(curr) else "cons")
        i += 1

    spelling = ""
    for text, seg_type in segments:
        if spelling and seg_type == "cons":
            last = spelling[-1]
            if text and text[0] == last:
                trimmed = text.lstrip(last)
                spelling += trimmed
                continue
        spelling += text

    if add_final_e and not spelling.endswith("e"):
        spelling += "e"

    return spelling, notes


def load_cmu(path: str) -> Dict[str, List[str]]:
    cmu: Dict[str, List[str]] = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip() or line.startswith(";;;"):
                continue
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            word_raw = parts[0].lower()
            word = re.sub(r"\(\d+\)$", "", word_raw)
            phonemes = parts[1:]
            if word not in cmu:  # keep first occurrence
                cmu[word] = phonemes
    return cmu


def match_case(original: str, simplified: str) -> str:
    if original.isupper():
        return simplified.upper()
    if original[0].isupper():
        return simplified.capitalize()
    return simplified


def simplify_word(word: str, cmu: Dict[str, List[str]]) -> str:
    clean = word.strip()
    if not clean:
        return clean
    key = re.sub(r"[^A-Za-z']+", "", clean).lower()
    if not key:
        return clean

    if key in FORCED_OVERRIDE:
        return match_case(clean, FORCED_OVERRIDE[key])

    phonemes = (
        cmu.get(key)
        or cmu.get(re.sub(r"'s$", "", key))
        or FALLBACK_LEXICON.get(key)
    )
    if not phonemes:
        return clean  # unknown: leave unchanged

    spelling, notes = phonemes_to_simplified(phonemes)
    should_change = bool(notes) or bool(COMPLEX_PATTERN.search(key))
    final_spelling = spelling if should_change else clean.lower()
    return match_case(clean, final_spelling)


def modernize_text(text: str, cmu: Dict[str, List[str]]) -> str:
    def repl(match: re.Match) -> str:
        token = match.group(0)
        return simplify_word(token, cmu)

    # Replace only word tokens, preserve punctuation/spacing.
    return re.sub(r"[A-Za-z']+", repl, text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simplify English spelling using CMU pronunciations.")
    parser.add_argument(
        "--dict",
        dest="dict_path",
        required=True,
        help="Path to CMU dictionary file (e.g., CMU.txt).",
    )
    args = parser.parse_args()

    try:
        cmu = load_cmu(args.dict_path)
    except FileNotFoundError:
        print(f"Dictionary not found: {args.dict_path}", file=sys.stderr)
        sys.exit(1)

    data = sys.stdin.read()
    output = modernize_text(data, cmu)
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
