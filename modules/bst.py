class BSTNode:
    """
    узел бинарного дерева поиска (температура и список дат)
    """
    def __init__(self, temperature, date):
        """
        функция __init__ создаёт узел дерева с температурой и датой

        параметры:
        temperature: температура (ключ)
        date: дата
        
        возвращает:
        None
        """
        self.temperature = temperature
        self.dates = [date] #список дат с такой температурой
        self.left = None #левый потомок (меньшая температура)
        self.right = None #правый потомок (большая температура)

class BinarySearchTree:
    """
    бинарное дерево поиска для хранения температур и дат
    """
    def __init__(self):
        """
        функция __init__ создаёт пустое бинарное дерево поиска
        
        возвращает:
        None
        """
        self.root = None

    def insert(self, temperature, date):
        """
        функция insert вставляет новую пару (температура, дата) в дерево

        параметры:
        temperature: температура (ключ)
        date: дата
        
        возвращает:
        None
        """
        if self.root is None:
            self.root = BSTNode(temperature, date) #создаю корень
        else:
            self._insert_recursive(self.root, temperature, date)

    def _insert_recursive(self, node, temperature, date):
        """
        функция _insert_recursive рекурсивно вставляет элемент, сравнивает температуру и идёт влево или вправо

        параметры:
        node: текущий узел
        temperature: температура
        date: дата
        
        возвращает:
        None
        """
        if temperature < node.temperature:
            if node.left is None:
                node.left = BSTNode(temperature, date) #создаю левого потомка
            else:
                self._insert_recursive(node.left, temperature, date)
        elif temperature > node.temperature:
            if node.right is None:
                node.right = BSTNode(temperature, date) #создаю правого потомка
            else:
                self._insert_recursive(node.right, temperature, date)
        else:
            #если температура уже есть в дереве, добавляю дату в существующий узел
            node.dates.append(date)

    def find_above_threshold(self, threshold):
        """
        функция find_above_threshold возвращает список всех дней с температурой выше заданного порога

        параметры:
        threshold: порог температуры
        
        возвращает:
        список пар (температура, дата)
        """
        result = []
        self._find_above_recursive(self.root, threshold, result)
        return result

    def _find_above_recursive(self, node, threshold, result):
        """
        функция _find_above_recursive рекурсивно обходит, собирает дни с температурой выше порога

        параметры:
        node: текущий узел
        threshold: порог температуры
        result: список для накопления результатов
        
        возвращает:
        None
        """
        if node is None:
            return
        if node.temperature > threshold:
            #идём влево (там могут быть температуры ниже порога)
            self._find_above_recursive(node.left, threshold, result)
            for date in node.dates:
                result.append((node.temperature, date)) #добавляем текущий узел
            #идём вправо (там все температуры точно выше порога)
            self._find_above_recursive(node.right, threshold, result)
        else:
            #если текущий узел меньше или равен порогу, то всё левое поддерево тоже меньше или равно порогу
            self._find_above_recursive(node.right, threshold, result)#идём только вправо
