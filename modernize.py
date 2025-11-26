#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List


def load_dictionary(path: Path) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split(maxsplit=1)
            if len(parts) != 2:
                continue
            word, american = parts
            mapping[word.lower()] = american
    return mapping


def load_rules(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def apply_rules(word: str, rules: List[Dict[str, str]]) -> str:
    result = word
    for rule in rules:
        pattern = rule.get("pattern")
        replacement = rule.get("replacement", "")
        try:
            result = re.sub(pattern, replacement, result)
        except re.error:
            # skip malformed rule
            continue
    return result


def tokenize_text(text: str) -> List[str]:
    pattern = re.compile(r"[A-Za-z]+|\s+|.", re.DOTALL)
    return [match.group(0) for match in pattern.finditer(text)]


def apply_casing(original: str, new: str) -> str:
    if original.isupper():
        return new.upper()
    if original.istitle():
        return new.title()
    return new


def convert_tokens(tokens: List[str],
                   dictionary: Dict[str, str],
                   rules: List[Dict[str, str]]) -> List[str]:
    out: List[str] = []
    for token in tokens:
        if token.isalpha():
            w = token.lower()

            if w in dictionary:
                converted = apply_rules(dictionary[w], rules)
            else:
                converted = apply_rules(w, rules)

            converted = apply_casing(token, converted)
            out.append(converted)
        else:
            out.append(token)
    return out


def save_output(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert text to Americanized spelling.")
    parser.add_argument("--dict", required=True, help="Path to American dictionary.")
    parser.add_argument("--rules", required=False, help="Path to rule-map.json rules.")
    parser.add_argument("--input", help="Input text. If omitted, reads from stdin.")
    parser.add_argument("--out", help="Output file.")

    args = parser.parse_args()

    dictionary = load_dictionary(Path(args.dict))

    if args.rules:

        rules = load_rules(Path(args.rules))
    else:
        rules = load_rules(Path("./rules.json"))

    text = args.input if args.input is not None else sys.stdin.read()

    tokens = tokenize_text(text)
    converted_tokens = convert_tokens(tokens, dictionary, rules)

    output_text = "".join(converted_tokens)

    if args.out:
        save_output(Path(args.out), output_text)
    else:
        sys.stdout.write(output_text)


if __name__ == "__main__":
    main()
