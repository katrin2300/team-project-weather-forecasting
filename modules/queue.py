class Node:
    """
    Узел односвязного списка для очереди
    атрибуты:
        data - данные, которые храним в узле
        next - ссылка на следующий узел
    """
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    """
    Очередь на основе односвязного списка.
    Нужна для хранения значений при вычислении скользящего среднего
    """
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def enqueue(self, item):
        """
        Добавляет элемент в конец очереди

        параметры:
            item - значение, которое нужно добавить
        """
        new_node = Node(item)
        if self.is_empty():  # проверяем, пустая ли очередь, если очередь пустая, то новый элемент становится его началом и концом
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):
        """
        Удаляет элемент из начала очереди и возвращает его
        """
        if self.is_empty():
            raise IndexError('empty queue')
        item = self.front.data
        self.front = self.front.next
        self._size -= 1
        if self.is_empty():
            self.rear = None
        return item

    def is_empty(self):
        """
        Проверяет, пустая ли очередь
        """
        return self._size == 0

    def size(self):
        """
        Возвращает количество элементов в очереди
        """
        return self._size

    def get_all_values(self):
        """
        Возвращает список всех значений в порядке от начала до конца
        """
        values = []
        current = self.front  # начинаем обход с первого элемента
        while current:  # проходим по всем узлам
            values.append(current.data)
            current = current.next
        return values

    def __str__(self):
        """
        Возвращает строковое представление списка
        """
        if self.is_empty():
            return "Queue([])"
        values = []  # список, в который будем сохранять значения
        current = self.front
        while current:
            values.append(str(current.data))
            current = current.next
        return f"Queue([{', '.join(values)}])"
