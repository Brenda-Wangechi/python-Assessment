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


def identify_most_common_word(text: str) -> str | None:
    words = [w.lower() for w in tokenize_words(text)]
    if not words:
        return None
    counts = Counter(words)
    most_common = counts.most_common(1)
    return most_common[0][0] if most_common else None


def average_word_length(text: str) -> float:
    words = tokenize_words(text)
    if not words:
        return 0
    total_len = sum(len(w) for w in words)
    return total_len / len(words)


def calculate_average_word_length(text: str) -> float:
    return average_word_length(text)


def count_paragraphs(text: str) -> int:
    raw_paragraphs = re.split(r"\n{2,}", text)
    count = 0
    index = 0
    while index < len(raw_paragraphs):
        if raw_paragraphs[index].strip():
            count += 1
        index += 1
    return count


def count_sentences(text: str) -> int:
    # A simple heuristic: count terminal punctuation groups as sentence boundaries
    if not text.strip():
        return 1
    candidates = SENTENCE_RE.findall(text)
    return max(1, len(candidates))


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


class Book:
    def __init__(self, title: str, page_count: int):
        if not title:
            raise ValueError("title is required")
        self.title = title
        # use the property setter to validate
        self._page_count = None
        self.page_count = page_count

    @property
    def page_count(self) -> int | None:
        return self._page_count

    @page_count.setter
    def page_count(self, value):
        if not isinstance(value, int):
            print("page_count must be an integer")
            self._page_count = None
        else:
            self._page_count = value

    def turn_page(self) -> None:
        print("Flipping the page...wow, you read fast!")


class Coffee:
    VALID_SIZES = {"Small", "Medium", "Large"}

    def __init__(self, size: str, price: float):
        if not size:
            raise ValueError("size is required")
        if price is None:
            raise ValueError("price is required")
        self._size = None
        self.size = size
        self.price = float(price)

    @property
    def size(self) -> str:
        return self._size

    @size.setter
    def size(self, value: str) -> None:
        if value not in self.VALID_SIZES:
            print("size must be Small, Medium, or Large")
            self._size = None
        else:
            self._size = value

    def tip(self) -> None:
        print("This coffee is great, here's a tip!")
        try:
            self.price = float(self.price) + 1
        except Exception:
            # if price is somehow invalid, set to 1 higher from 0
            self.price = 1.0


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Text analysis for a news article file.")
    p.add_argument("--file", "-f", help="Path to article text file", required=True)
    p.add_argument("--word", "-w", help="Specific word to count occurrences of")
    p.add_argument("--top", "-t", help="Show top N most common words", type=int, default=5)
    p.add_argument("--case-sensitive", action="store_true", help="Count word with case-sensitivity")
    p.add_argument("--no-stopwords", action="store_true", help="Do not filter common stopwords from top results")
    p.add_argument("--demo", action="store_true", help="Run demo of Book and Coffee classes")
    args = p.parse_args(argv)

    try:
        text = read_text(args.file)
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}")
        return 2

    if args.demo:
        def demo_usage():
            print("--- Demo: Book and Coffee ---")
            b = Book(title="The Hobbit", page_count=310)
            print(f"Created Book: title={b.title}, page_count={b.page_count}")
            b.turn_page()

            c = Coffee(size="Medium", price=3.5)
            print(f"Created Coffee: size={c.size}, price={c.price}")
            c.tip()
            print(f"Coffee price after tip: {c.price}")
            print("--- End Demo ---")

        demo_usage()
        return 0

    # Run analysis
    result = analyze(text, word=args.word, top_n=args.top, case_sensitive=args.case_sensitive, ignore_stopwords=not args.no_stopwords)
    print_analysis(result, word=args.word)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
