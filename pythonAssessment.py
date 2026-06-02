#!/usr/bin/env python3
"""
pythonAssessment.py

Text analysis utilities for a news article file.

Features:
- Count occurrences of a specific word
- Identify most common word(s)
- Calculate average word length
- Count paragraphs
- Count sentences

Usage: run `python3 pythonAssessment.py --file sample_article.txt`
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from typing import List, Tuple


WORD_RE = re.compile(r"\b[\w']+\b")
SENTENCE_RE = re.compile(r"[.!?]+")


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def tokenize_words(text: str) -> List[str]:
    return WORD_RE.findall(text)


def count_specific_word(text: str, word: str, case_sensitive: bool = False) -> int:
    if not case_sensitive:
        text = text.lower()
        word = word.lower()
    words = tokenize_words(text)
    return sum(1 for w in words if w == word)


def most_common_words(text: str, top_n: int = 1, ignore_stopwords: bool = True) -> List[Tuple[str, int]]:
    words = [w.lower() for w in tokenize_words(text)]
    if ignore_stopwords:
        STOPWORDS = {
            "the", "and", "a", "an", "in", "on", "at", "for", "to", "of", "is", "are",
            "was", "were", "that", "it", "as", "with", "by", "from", "be", "this",
        }
        words = [w for w in words if w not in STOPWORDS]
    counts = Counter(words)
    return counts.most_common(top_n)


def average_word_length(text: str) -> float:
    words = tokenize_words(text)
    if not words:
        return 0.0
    total_len = sum(len(w) for w in words)
    return total_len / len(words)


def count_paragraphs(text: str) -> int:
    paragraphs = [p for p in re.split(r"\n{2,}", text) if p.strip()]
    return len(paragraphs)


def count_sentences(text: str) -> int:
    # A simple heuristic: count terminal punctuation groups as sentence boundaries
    candidates = SENTENCE_RE.findall(text)
    return len(candidates)


def analyze(text: str, word: str = None, top_n: int = 1, case_sensitive: bool = False, ignore_stopwords: bool = True) -> dict:
    result = {}
    result["word_count"] = len(tokenize_words(text))
    result["avg_word_length"] = average_word_length(text)
    result["paragraphs"] = count_paragraphs(text)
    result["sentences"] = count_sentences(text)
    if word:
        result["specific_word_occurrences"] = count_specific_word(text, word, case_sensitive=case_sensitive)
    result["top_words"] = most_common_words(text, top_n, ignore_stopwords=ignore_stopwords)
    return result


def print_analysis(result: dict, word: str = None) -> None:
    print(f"Total words: {result['word_count']}")
    print(f"Average word length: {result['avg_word_length']:.2f}")
    print(f"Paragraphs: {result['paragraphs']}")
    print(f"Sentences: {result['sentences']}")
    if word and "specific_word_occurrences" in result:
        print(f"Occurrences of '{word}': {result['specific_word_occurrences']}")
    print("Top words:")
    for w, c in result["top_words"]:
        print(f"  {w}: {c}")


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Text analysis for a news article file.")
    p.add_argument("--file", "-f", help="Path to article text file", required=True)
    p.add_argument("--word", "-w", help="Specific word to count occurrences of")
    p.add_argument("--top", "-t", help="Show top N most common words", type=int, default=5)
    p.add_argument("--case-sensitive", action="store_true", help="Count word with case-sensitivity")
    p.add_argument("--no-stopwords", action="store_true", help="Do not filter common stopwords from top results")
    args = p.parse_args(argv)

    try:
        text = read_text(args.file)
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}")
        return 2

    # Run analysis
    result = analyze(text, word=args.word, top_n=args.top, case_sensitive=args.case_sensitive, ignore_stopwords=not args.no_stopwords)
    print_analysis(result, word=args.word)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
