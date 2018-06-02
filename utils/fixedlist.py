class FixedList(list):
    def __init__(self, maximum_item_count: int):
        self.max_items = maximum_item_count

    def append(self, *items):
        for item in items:
            if super().__len__() >= self.max_items:
                super().pop(0)

            super().append(item)
