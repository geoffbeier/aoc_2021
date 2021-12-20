class BitArray:
    n: int
    w: int

    def __init__(self, bits: str = None, one: str = "1", zero: str = "0"):
        self.n = 0
        self.w = 1
        if bits:
            self.w = len(bits)
            for i, b in enumerate(bits):
                if b == one:
                    self.set(i)
                elif b == zero:
                    pass
                else:
                    raise ValueError(f"{bits} is not a valid bitstring")

    def set(self, pos: int):
        self.n |= 1 << (self.w - 1 - pos)

    def clear(self, pos: int):
        self.n &= ~(1 << (self.w - 1 - pos))

    def get(self, pos: int, default=None):
        if pos >= self.w:
            return default
        return self.n >> (self.w - 1 - pos) & 1

    def expand_right(self, count: int, fill: int = 0):
        self.n = self.n << count
        self.w += count
        if fill:
            for i in range(count):
                self.n |= 1 << i

    def expand_left(self, count: int, fill: int = 0):
        self.w += count
        if fill:
            for i in range(count):
                self.n |= 1 << (self.w - 1 - i)

    def count(self):
        return self.n.bit_count()

    def copy(self):
        ba = BitArray()
        ba.w = self.w
        ba.n = self.n
        return ba

    def __getitem__(self, key: int):
        if key >= self.w:
            raise KeyError(f"Invalid index {key} into {self.w}-bit wide array")
        return self.get(key)

    def __setitem__(self, key: int, value: int):
        if value == 0:
            self.clear(key)
        else:
            self.set(key)

    def __str__(self):
        return f"{self.n: 0{self.w + 1}b}"
