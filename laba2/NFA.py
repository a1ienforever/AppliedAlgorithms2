from laba2.test import transitions


class NFA:
    def __init__(self, transitions, start_state, accept_states):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def _epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)

        while stack:
            state = stack.pop()
            for next_state in self.transitions.get((state, "e"), []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def accepts_substring(self, string):
        for start_pos in range(len(string)):
            if self._accepts_from_position(string[start_pos:]):
                return True
        return False

    def _accepts_from_position(self, substring):
        current_states = self._epsilon_closure({self.start_state})

        for symbol in substring:
            next_states = set()
            for state in current_states:
                next_states.update(self.transitions.get((state, symbol), []))
            current_states = self._epsilon_closure(next_states)
            if any(state in self.accept_states for state in current_states):
                return True

        return any(state in self.accept_states for state in current_states)



nfa = NFA(transitions=transitions, start_state="q0", accept_states={"q6", "q7"})

print(nfa.accepts_substring("01"))
print(nfa.accepts_substring("0110"))
print(nfa.accepts_substring("01101"))
print(nfa.accepts_substring("010"))
print(nfa.accepts_substring("101100011"))
