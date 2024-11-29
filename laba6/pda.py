class StateMachine:
    """
    Базовый класс конечного автомата.
    """

    def __init__(self, alphabet, init_state_id, end_state_id, states):
        self.alphabet = alphabet
        self.init_state_id = init_state_id
        self.end_state_id = end_state_id
        self.states = states

    def set_init_state_id(self, init_state_id):
        """
        Установить начальное состояние.
        """
        self.init_state_id = init_state_id


class Fsm(StateMachine):
    """
    Расширенный конечный автомат с памятью и правилами переходов.
    """

    def __init__(self, alphabet=None, init_state_id=0, end_state_id=0, states=None, end_rule=None):
        super().__init__(alphabet or [], init_state_id, end_state_id, states or [])
        self.current_state_id = init_state_id
        self.memory = []  # Память автомата
        self.tree = []  # Дерево переходов
        self.end_rule = end_rule or (lambda state_id, memory: {"state_id": -1, "memory": []})

    def set_init_state_id(self, init_state_id=0):
        """
        Установить начальное состояние.
        """
        super().set_init_state_id(init_state_id)
        self.current_state_id = init_state_id

    def set_end_rule(self, end_rule=None):
        """
        Установить заключительное правило.
        """
        self.end_rule = end_rule or (lambda state_id, memory: {"state_id": -1, "memory": []})

    def clear(self):
        """
        Сброс состояния автомата.
        """
        self.current_state_id = self.init_state_id
        self.memory = []
        self.tree = []

    def check_string(self, string):
        """
        Проверка строки: состоит ли она только из символов алфавита.
        """
        return all(ch in self.alphabet for ch in string)

    def run(self, string=''):
        """
        Запустить автомат с переданной строкой.
        """
        self.current_state_id = self.init_state_id
        if self.check_string(string):
            for ch in string:
                # Найти текущее состояние
                state = next((s for s in self.states if s.get("state_id") == self.current_state_id), {})
                rule = state.get("rule", lambda ch, memory, tree: {"state_id": -1, "memory": [], "tree": []})

                # Применить правило перехода
                transition = rule(ch, self.memory, self.tree)
                self.current_state_id = transition.get("state_id", -1)
                self.memory = transition.get("memory", [])
                self.tree = transition.get("tree", [])

            # Применить заключительное правило
            end_result = self.end_rule(self.current_state_id, self.memory)
            self.current_state_id = end_result.get("state_id", -1)
            self.memory = end_result.get("memory", [])

            # Определить результат
            result = self.current_state_id == self.end_state_id
            tree = self.tree
            self.clear()
            return {"result": result, "tree": tree}
        else:
            return {"result": "invalid string"}


# Пример использования
if __name__ == "__main__":
    # Определение состояний автомата
    states = [
        {
            "state_id": 0,
            "rule": lambda ch, memory, tree: {
                "state_id": 1 if ch == 'a' else -1,
                "memory": memory + [ch],
                "tree": tree + [(0, 1, ch)]
            },
        },
        {
            "state_id": 1,
            "rule": lambda ch, memory, tree: {
                "state_id": 2 if ch == 'b' else -1,
                "memory": memory + [ch],
                "tree": tree + [(1, 2, ch)]
            },
        },
    ]

    # Создание автомата
    fsm = Fsm(
        alphabet=['a', 'b'],
        init_state_id=0,
        end_state_id=2,
        states=states,
        end_rule=lambda state_id, memory: {"state_id": 2 if state_id == 2 else -1, "memory": memory}
    )

    # Тестовые строки
    test_strings = ["ab", "abab", "a", "b"]
    for string in test_strings:
        result = fsm.run(string)
        print(f"Строка '{string}': {'допустима' if result['result'] else 'недопустима'}, дерево: {result['tree']}")
