import csv


class TuringMachine:
    def __init__(self, tape, transitions, initial_state, final_states):
        self.tape = list(
            tape
        )  # преобразуем строку в список для возможности модификации
        self.head = 0  # позиция головки
        self.state = initial_state  # начальное состояние
        self.transitions = transitions  # словарь переходов
        self.final_states = final_states  # конечные состояния

    def run(self):
        while self.state not in self.final_states:  # пока не в конечном состоянии
            current_symbol = self.tape[self.head]  # символ на текущей позиции
            if (self.state, current_symbol) not in self.transitions:
                print("Нет перехода, программа остановлена.")
                return
            action = self.transitions[(self.state, current_symbol)]
            new_symbol, move, new_state = (
                action  # определение нового символа, движения и состояния
            )
            self.tape[self.head] = new_symbol  # записываем новый символ
            self.head += (
                1 if move == "R" else -1
            )
            self.state = new_state

        print("Программа завершена.")


def load_transitions_from_csv(filename):
    transitions = {}
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                current_state, current_symbol, new_symbol, move, new_state = row
                transitions[(current_state, current_symbol)] = (
                    new_symbol,
                    move,
                    new_state,
                )
    return transitions


if __name__ == "__main__":
    tape = input("Введите содержимое ленты: ")

    path = "C:\\Users\\artyo\\PycharmProjects\\AppliedAlgorithms2\\laba9\\input_file.csv"
    transitions = load_transitions_from_csv(path)

    initial_state = "q0"
    final_states = {"q2"}

    tm = TuringMachine(tape, transitions, initial_state, final_states)
    tm.run()

    print("Лента после выполнения:", "".join(tm.tape))
