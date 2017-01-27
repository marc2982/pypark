
class Directory(object):

    """Holds a reference to all game objects in the world."""

    def __init__(self):
        self.shops = []

    def add_shop(self, position):
        self.shops.append(Shop(position))

    def remove_shop(self, position):
        for i, shop in enumerate(self.shops):
            if shop.position == position:
                self.shops.pop(i)


class Shop(object):

    """temp object for testing, will be fleshed out and moved later."""

    def __init__(self, position):
        self.position = position  # world tile index

    def __str__(self):
        return str(self.position)
    __repr__ = __str__
