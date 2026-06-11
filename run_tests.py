import sys
import io
from contextlib import redirect_stdout

from lib.book import Book
from lib.coffee import Coffee

errors = []

def expect(cond, msg):
    if not cond:
        errors.append(msg)


def capture(func, *args, **kwargs):
    buf = io.StringIO()
    with redirect_stdout(buf):
        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            return buf.getvalue(), e
    return buf.getvalue(), None


def test_book():
    b = Book("The Hobbit", 310)
    expect(b.title == "The Hobbit", "Book title not set correctly")
    expect(b.page_count == 310, "Book page_count not set correctly")

    out, err = capture(Book, "NoInt", "not-an-int")
    expect("page_count must be an integer" in out, "Book did not print page_count message on non-int")

    out, err = capture(b.turn_page)
    expect("Flipping the page...wow, you read fast!" in out, "turn_page() did not print expected message")


def test_coffee():
    c = Coffee("Medium", "brewed", price=3)
    expect(c.size == "Medium", "Coffee size not set correctly")
    expect(c.status == "brewed", "Coffee status not set correctly")

    out, err = capture(Coffee, "X", "cold")
    expect("size must be Small, Medium, or Large" in out, "Coffee did not print size error message")

    out, err = capture(c.repair)
    expect("repaired" in out.lower(), "repair() did not report that the shoe was repaired")

    old = c.price
    c.add_price()
    expect(c.price == old + 1, "add_price() did not increment price by 1")


def main():
    test_book()
    test_coffee()

    if errors:
        print("FAILED TESTS:")
        for e in errors:
            print("-", e)
        sys.exit(1)
    else:
        print("All tests passed")


if __name__ == "__main__":
    main()
