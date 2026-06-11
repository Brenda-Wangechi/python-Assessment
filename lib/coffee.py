class Coffee:
    VALID_SIZES = ("Small", "Medium", "Large")

    def __init__(self, size, status=None, price=0):
        # allow callers to pass (size, price) as second positional arg
        if isinstance(status, (int, float)) and price == 0:
            price = status
            status = None

        if size not in self.VALID_SIZES:
            print("size must be Small, Medium, or Large")
        self.size = size
        self.status = status
        self.price = price

    def repair(self):
        print("Your shoe has been repaired")

    def tip(self, amount=1):
        print("This coffee is great, here\u2019s a tip!")
        try:
            self.price += amount
        except Exception:
            self.price = amount

    # keep legacy name
    def add_price(self):
        self.tip(1)
