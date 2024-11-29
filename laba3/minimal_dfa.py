from typing import Set, Dict, Tuple, List, FrozenSet

class DFA:
    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transition_function: Dict[Tuple[str, str], str],
        start_state: str,
        final_states: Set[str],
    ):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.final_states = final_states

    def minimize(self) -> 'DFA':

        partition: List[Set[str]] = [self.final_states, self.states - self.final_states]
        work_list: List[Set[str]] = [self.final_states]

        while work_list:
            A = work_list.pop()
            for symbol in self.alphabet:
                X = {state for state in self.states if self.transition_function.get((state, symbol)) in A}

                new_P = []
                for Y in partition:
                    intersection = Y.intersection(X)
                    difference = Y.difference(X)

                    if intersection and difference:
                        new_P.append(intersection)
                        new_P.append(difference)

                        if Y in work_list:
                            work_list.remove(Y)
                            work_list.append(intersection)
                            work_list.append(difference)
                        else:
                            if len(intersection) <= len(difference):
                                work_list.append(intersection)
                            else:
                                work_list.append(difference)
                    else:
                        new_P.append(Y)

                partition = new_P

        new_states = {frozenset(group) for group in partition}
        new_start_state = next(frozenset(group) for group in partition if self.start_state in group)
        new_final_states = {frozenset(group) for group in partition if group & self.final_states}

        new_transition_function = {}
        for group in partition:
            representative = next(iter(group))
            for symbol in self.alphabet:
                target = self.transition_function.get((representative, symbol))
                if target:
                    target_group = next(frozenset(g) for g in partition if target in g)
                    new_transition_function[(frozenset(group), symbol)] = frozenset(target_group)

        return DFA(
            states=new_states,
            alphabet=self.alphabet,
            transition_function=new_transition_function,
            start_state=new_start_state,
            final_states=new_final_states,
        )

    def __str__(self) -> str:

        header = "State\t" + "\t".join(self.alphabet) + "\n"
        rows = []

        for state in self.states:
            row = [str(state)]
            for symbol in self.alphabet:
                target = self.transition_function.get((state, symbol), "-")
                row.append(str(target))
            rows.append("\t".join(row))

        transition_table = header + "\n".join(rows)
        start = f"Start State: {self.start_state}"
        finals = f"Final States: {self.final_states}"

        return f"Transition Table:\n{transition_table}\n\n{start}\n{finals}"


if __name__ == "__main__":
    dfa = DFA(
        states={"A", "B", "C", "D", "E", "F"},
        alphabet={"0", "1"},
        transition_function={
            ("A", "0"): "B",
            ("A", "1"): "C",
            ("B", "0"): "A",
            ("B", "1"): "D",
            ("C", "0"): "E",
            ("C", "1"): "F",
            ("D", "0"): "E",
            ("D", "1"): "F",
            ("E", "0"): "E",
            ("E", "1"): "F",
            ("F", "0"): "F",
            ("F", "1"): "F",
        },
        start_state="A",
        final_states={"E", "F"},
    )

    print("Исходный ДКА:")
    print(dfa)

    minimized_dfa = dfa.minimize()

    print("\nМинимизированный ДКА:")
    print(minimized_dfa)
