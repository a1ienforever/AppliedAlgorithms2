import csv
from anytree import Node, RenderTree

class ParseTreeGenerator:
    def __init__(self, grammar, start_symbol):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.tree_root = None

    def parse(self, input_string):
        self.tree_root = Node(self.start_symbol)
        success, remaining = self._parse_recursive(self.start_symbol, input_string, self.tree_root)
        return success and not remaining

    def _parse_recursive(self, non_terminal, input_string, parent_node):
        if non_terminal not in self.grammar:
            if input_string.startswith(non_terminal):
                Node(non_terminal, parent=parent_node)
                return True, input_string[len(non_terminal):]
            return False, input_string

        for production in self.grammar[non_terminal]:
            current_node = Node(non_terminal, parent=parent_node)
            remaining_string = input_string
            success = True

            for symbol in production:
                result, remaining_string = self._parse_recursive(symbol, remaining_string, current_node)
                if not result:
                    success = False
                    break

            if success:
                return True, remaining_string

            current_node.parent = None

        return False, input_string

    def render_tree(self):
        if not self.tree_root:
            print("Дерево разбора отсутствует.")
        else:
            for pre, fill, node in RenderTree(self.tree_root):
                print(f"{pre}{node.name}")

    def save_tree_to_csv(self, file_path):
        if not self.tree_root:
            print("Дерево разбора отсутствует. Нечего сохранять.")
            return

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Parent", "Node"])
            for node in self.tree_root.descendants:
                writer.writerow([node.parent.name if node.parent else "", node.name])



grammar = {
    "S": [["A", "B"]],
    "A": [["a"]],
    "B": [["b", "C"]],
    "C": [["c"]]
}

start_symbol = "S"
input_string = "abc"

# Создаём генератор дерева разбора
parser = ParseTreeGenerator(grammar, start_symbol)

# Парсим строку
if parser.parse(input_string):
    print("Строка разобрана успешно.")
    print("Дерево разбора:")
    parser.render_tree()

    # Сохраняем дерево в CSV
    csv_file = "parse_tree.csv"
    parser.save_tree_to_csv(csv_file)
    print(f"Дерево разбора сохранено в {csv_file}.")
else:
    print("Ошибка разбора строки.")
