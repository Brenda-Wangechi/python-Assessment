class Coffee:
    VALID_SIZES = ("Small", "Medium", "Large")

    def __init__(self, size, status, price=0):
        if size not in self.VALID_SIZES:
            print("size must be Small, Medium, or Large")
        self.size = size
        self.status = status
        self.price = price

    def repair(self):
        print("Your shoe has been repaired")

    def add_price(self):
        try:
            self.price += 1
        except Exception:
            self.price = 1
