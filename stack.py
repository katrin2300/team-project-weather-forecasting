class Stack:
    def __init__(self):
        self.items = []

    def push(self, data):
        self.items.append(data)

    def pop(self):
        if self.is_empty():
            raise IndexError("empty stack")
        return self.items.pop()

    def size(self):
        return len(self.items)

    def is_empty(self):
        return len(self.items) == 0

    def peek(self):
        if self.is_empty():
            raise IndexError("empty stack")
        return self.items[-1]

    def __str__(self):
        return f"Stack({self.items})"