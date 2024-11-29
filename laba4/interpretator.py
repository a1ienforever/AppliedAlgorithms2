class State:
    """Класс для представления состояния автомата."""
    def __init__(self, is_final=False):
        self.is_final = is_final
        self.transitions = {}

    def add_transition(self, symbol, state):
        """Добавление перехода по символу."""
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]


class NFA:
    """Недетерминированный конечный автомат (НКА)."""
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state

    @staticmethod
    def concat(nfa1, nfa2):
        """Операция конкатенации двух НКА."""
        nfa1.accept_state.add_transition(None, nfa2.start_state)
        return NFA(nfa1.start_state, nfa2.accept_state)

    @staticmethod
    def union(nfa1, nfa2):
        """Операция объединения двух НКА (a|b)."""
        start = State()
        accept = State(is_final=True)
        start.add_transition(None, nfa1.start_state)
        start.add_transition(None, nfa2.start_state)
        nfa1.accept_state.add_transition(None, accept)
        nfa2.accept_state.add_transition(None, accept)
        return NFA(start, accept)

    @staticmethod
    def kleene_star(nfa):
        """Операция звезды Клини (a*)."""
        start = State()
        accept = State(is_final=True)
        start.add_transition(None, nfa.start_state)
        start.add_transition(None, accept)
        nfa.accept_state.add_transition(None, nfa.start_state)
        nfa.accept_state.add_transition(None, accept)
        return NFA(start, accept)

    @staticmethod
    def from_symbol(symbol):
        """Создание НКА для одного символа."""
        start = State()
        accept = State(is_final=True)
        start.add_transition(symbol, accept)
        return NFA(start, accept)


class NFAExecutor:
    """Исполнитель для симуляции работы НКА над строкой."""
    def __init__(self, nfa):
        self.nfa = nfa

    def match(self, text):
        """Проверка, принимает ли НКА строку."""
        current_states = self._epsilon_closure({self.nfa.start_state})
        for symbol in text:
            next_states = set()
            for state in current_states:
                if symbol in state.transitions:
                    for next_state in state.transitions[symbol]:
                        next_states.add(next_state)
            current_states = self._epsilon_closure(next_states)
        # Только если есть финальное состояние в `current_states`, строка считается совпадением
        return any(state.is_final for state in current_states)

    def _epsilon_closure(self, states):
        """Находит ε-замыкание множества состояний."""
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            if None in state.transitions:
                for next_state in state.transitions[None]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure


class RegexParser:
    """Парсер регулярных выражений для построения НКА."""
    def __init__(self, regex):
        self.regex = regex
        self.index = 0

    def parse(self):
        """Главная функция для запуска парсинга регулярного выражения."""
        nfa = self._expression()
        if self.index < len(self.regex):
            raise ValueError("Неожиданный символ в регулярном выражении")
        return nfa

    def _expression(self):
        """Обработка выражений с поддержкой альтернативы (|)."""
        nfa = self._term()
        while self._current_char() == '|':
            self.index += 1
            nfa = NFA.union(nfa, self._term())
        return nfa

    def _term(self):
        """Обработка конкатенации."""
        nfa = self._factor()
        while self._current_char() not in {None, '|', ')'}:
            nfa = NFA.concat(nfa, self._factor())
        return nfa

    def _factor(self):
        """Обработка символов и операций звезды Клини (*)."""
        nfa = self._base()
        while self._current_char() == '*':
            self.index += 1
            nfa = NFA.kleene_star(nfa)
        return nfa

    def _base(self):
        """Обработка базовых символов и подвыражений в скобках."""
        char = self._current_char()

        if char == '(':
            self.index += 1
            nfa = self._expression()
            if self._current_char() != ')':
                raise ValueError("Отсутствует закрывающая скобка")
            self.index += 1
            return nfa

        if char.isalnum():
            self.index += 1
            return NFA.from_symbol(char)

        raise ValueError(f"Неправильный символ: {char}")

    def _current_char(self):
        if self.index >= len(self.regex):
            return None
        return self.regex[self.index]


class NFAPatternMatcher:
    def __init__(self, regex):
        self.regex = regex
        parser = RegexParser(regex)
        self.nfa = parser.parse()
        self.executor = NFAExecutor(self.nfa)

    def find_matches(self, text):
        matches = []
        n = len(text)

        for i in range(n):
            current_substring = ""
            for j in range(i, n):
                current_substring += text[j]
                if self.executor.match(current_substring):
                    matches.append(i)
                    break
                elif not self._can_continue(current_substring):
                    break
        return matches

    def _can_continue(self, substring):
        current_states = self.executor._epsilon_closure({self.nfa.start_state})
        for symbol in substring:
            next_states = set()
            for state in current_states:
                if symbol in state.transitions:
                    next_states.update(state.transitions[symbol])
            current_states = self.executor._epsilon_closure(next_states)

        return bool(current_states)


class KMP:
    def __init__(self, pattern):
        self.pattern = pattern
        self.prefix_function = self._compute_prefix_function()

    def _compute_prefix_function(self):
        m = len(self.pattern)
        pi = [0] * m
        k = 0
        for i in range(1, m):
            while k > 0 and self.pattern[k] != self.pattern[i]:
                k = pi[k - 1]
            if self.pattern[k] == self.pattern[i]:
                k += 1
            pi[i] = k
        return pi

    def search(self, text):
        n = len(text)
        m = len(self.pattern)
        pi = self.prefix_function
        q = 0
        matches = []
        for i in range(n):
            while q > 0 and self.pattern[q] != text[i]:
                q = pi[q - 1]
            if self.pattern[q] == text[i]:
                q += 1
            if q == m:
                matches.append(i - m + 1)
                q = pi[q - 1]
        return matches


text = "ababbbabababab"
pattern = "(ab)"
matcher = NFAPatternMatcher(pattern)
matches = matcher.find_matches(text)

print(f"'{pattern}' с НКА: {matches}")

kmp = KMP("ab")
kmp_matches = kmp.search(text)
print(f"'{pattern}' с КМП: {kmp_matches}")
