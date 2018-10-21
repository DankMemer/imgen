class FixedList(list):
    def __init__(self, maximum_item_count: int):
        self.max_items = maximum_item_count

    def append(self, *items):
        for item in items:
            super().append(item)

            if super().__len__() >= self.max_items:
                super().pop(0)
