class Stack:
    """
    стек на основе списка для отмены последнего сглаживания
    """
    def __init__(self):
        """
        функция __init__ создаёт пустой стек

        возвращает:
        None
        """
        self.items = []

    def push(self, data):
        """
        функция push добавляет элемент на вершину стека

        параметры:
        data: элемент, который нужно добавить
        
        возвращает:
        None
        """
        self.items.append(data)

    def pop(self):
        """
        функция pop удаляет и возвращает верхний элемент стека
        
        возвращает:
        верхний элемент стека
        """
        if self.is_empty():
            raise IndexError("empty stack")
        return self.items.pop()

    def size(self):
        """
        функция size возвращает кол-во элементов в стеке

        возвращает:
        кол-во элементов
        """
        return len(self.items)

    def is_empty(self):
        """
        функция is_empty проверяет, пуст ли стек

        возвращает:
        True, если стек пуст, иначе False
        """
        return len(self.items) == 0

    def peek(self):
        """
        функция peek возвращает верхний элемент стека без его удаления

        возвращает:
        верхний элемент стека
        """
        if self.is_empty():
            raise IndexError("empty stack")
        return self.items[-1]

    def __str__(self):
        """
        функция __str__ возвращает строковое представление стека

        возвращает:
        строковое представление стека
        """
        return f"Stack({self.items})"
