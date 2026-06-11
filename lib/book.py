class Book:
    def __init__(self, title, page_count):
        self.title = title
        if not isinstance(page_count, int):
            print("page_count must be an integer")
        self.page_count = page_count

    def turn_page(self):
        print("Flipping the page...wow, you read fast!")
