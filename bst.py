class BSTNode:
    def __init__(self, temperature, date):
        self.temperature = temperature
        self.dates = [date]
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, temperature, date):
        if self.root is None:
            self.root = BSTNode(temperature, date)
        else:
            self._insert_recursive(self.root, temperature, date)

    def _insert_recursive(self, node, temperature, date):
        if temperature < node.temperature:
            if node.left is None:
                node.left = BSTNode(temperature, date)
            else:
                self._insert_recursive(node.left, temperature, date)
        elif temperature > node.temperature:
            if node.right is None:
                node.right = BSTNode(temperature, date)
            else:
                self._insert_recursive(node.right, temperature, date)
        else:
            node.dates.append(date)

    def find_above_threshold(self, threshold):
        result = []
        self._find_above_recursive(self.root, threshold, result)
        return result

    def _find_above_recursive(self, node, threshold, result):
        if node is None:
            return
        if node.temperature > threshold:
            self._find_above_recursive(node.left, threshold, result)
            for date in node.dates:
                result.append((node.temperature, date))
            self._find_above_recursive(node.right, threshold, result)
        else:
            self._find_above_recursive(node.right, threshold, result)