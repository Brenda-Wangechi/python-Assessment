# Bookstore objects

This repository contains two small classes used to model bookstore items:

- `lib.book.Book` — represents a book with `title` and `page_count`.
- `lib.coffee.Coffee` — represents a coffee with `size` and `price`.

Features:

- `Book` validates `page_count` and prints `page_count must be an integer` when invalid.
- `Book.turn_page()` prints `Flipping the page...wow, you read fast!`.
- `Coffee` validates `size` (allowed: Small, Medium, Large) and prints an error if invalid.
- `Coffee.tip()` prints `This coffee is great, here's a tip!` and increases `price` by 1.

Run tests locally (recommended inside a virtualenv):

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

There is also a tiny `run_tests.py` runner included which doesn't require pytest:

```bash
python3 run_tests.py
```
