class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError('empty queue')
        item = self.front.data
        self.front = self.front.next
        self._size -= 1
        if self.is_empty():
            self.rear = None
        return item

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def get_all_values(self):
        values = []
        current = self.front
        while current:
            values.append(current.data)
            current = current.next
        return values

    def __str__(self):
        if self.is_empty():
            return "Queue([])"
        values = []
        current = self.front
        while current:
            values.append(str(current.data))
            current = current.next
        return f"Queue([{', '.join(values)}])"
