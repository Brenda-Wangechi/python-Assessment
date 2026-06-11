from lib.book import Book
from lib.coffee import Coffee


def test_book_init_and_turn_page(capsys):
    b = Book("The Hobbit", 310)
    assert b.title == "The Hobbit"
    assert b.page_count == 310
    b.turn_page()
    captured = capsys.readouterr()
    assert "Flipping the page...wow, you read fast!" in captured.out


def test_book_page_count_invalid(capsys):
    Book("NoInt", "not-an-int")
    captured = capsys.readouterr()
    assert "page_count must be an integer" in captured.out


def test_coffee_init_and_tip(capsys):
    c = Coffee("Medium", "brewed", price=3)
    assert c.size == "Medium"
    assert c.price == 3
    c.tip()
    captured = capsys.readouterr()
    assert "This coffee is great, here's a tip!" in captured.out
    assert c.price == 4


def test_coffee_size_invalid(capsys):
    Coffee("X", "cold")
    captured = capsys.readouterr()
    assert "size must be Small, Medium, or Large" in captured.out
