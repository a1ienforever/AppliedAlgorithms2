import csv


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def process(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                return False
        return current_state in self.final_states


def read_dfa_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        states = set()
        alphabet = set()
        transitions = {}
        start_state = None
        final_states = set()

        for row in reader:
            current_state, symbol, next_state = row[0], row[1], row[2]
            states.add(current_state)
            states.add(next_state)
            alphabet.add(symbol)
            transitions[(current_state, symbol)] = next_state


        start_state = input("Введите начальное состояние: ")
        final_states = set(input("Введите финальные состояния (через запятую): ").split(','))

        return DFA(states, alphabet, transitions, start_state, final_states)


def main():
    # Чтение автомата из CSV файла
    file_path = 'C:\\Users\\artyo\\PycharmProjects\\AppliedAlgorithms2\\laba1\\input_file.csv'
    dfa = read_dfa_from_csv(file_path)

    # Ввод и проверка цепочек
    while True:
        input_string = input("Введите цепочку для проверки (или 'exit' для выхода): ")
        if input_string == 'exit':
            break
        if dfa.process(input_string):
            print(f"Цепочка '{input_string}' допускается автоматом (начинается с '101').")
        else:
            print(f"Цепочка '{input_string}' не допускается автоматом (не начинается с '101').")


if __name__ == "__main__":
    main()
