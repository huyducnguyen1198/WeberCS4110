#!/usr/bin/env python



class State:
    def __init__(self, name: str = ""):
        self.name = name
        self.transitions = {}

    def add_transition(self, old_symbol, new_symbol, direction, new_state):
        if old_symbol in self.transitions:
            print("Error: Transition already exists")
            return

        self.transitions[old_symbol] = {
            "new_state": new_state,
            "new_symbol": new_symbol,
            "direction": direction
        }
    def hasTransition(self, old_symbol):
        if old_symbol in self.transitions:
            return True
        return False

    def getTransition(self, old_symbol):
        if self.hasTransition(old_symbol):
            return self.transitions[old_symbol]
        return None


    def __repr__(self):
        s = f'{self.name}: \n'
        for key, value in self.transitions.items():
            s += f'\t{key} -> {value}\n'
        return s


class TuringMachine:
    def __init__(self):
        self.states = {}
        self.tape = []
        self.head = 0
        self.current_state = None
        self.numTransitions = 0
        self.maxTransitions = 1000

    def add_state(self, state: State):
        self.states[state.name] = state

    def hasState(self, stateName: str):
        return stateName in self.states

    def getState(self, stateName: str):
        return self.states[stateName] if self.hasState(stateName) else None

    def run(self, tape: str):
        self.tape = list(tape)
        self.head = 0
        self.current_state = self.states["1 Start"]
        while True:
            print(self.tape, self.head, self.current_state.name)
            # check if current state is halt => accept
            if "Halt" in self.current_state.name:
                print("Accepted")
                break

            # check is there is a transition for current state
            # if not => reject
            print(self.tape, self.head, self.current_state.name)
            if self.head >= len(self.tape):
                self.tape.append("_")
            trans = self.current_state.getTransition(self.tape[self.head])
            if trans is None:
                print("Rejected")
                break

            # Change current state
            self.tape[self.head] = trans["new_symbol"]

            # Move head
            # If move left when head is at 0 => reject
            direction = trans["direction"]
            if direction == "R":
                self.head += 1
            elif direction == "L":
                self.head -= 1
            if self.head < 0:
                print("Rejected")
                break
            self.numTransitions += 1

            # Change current state
            self.current_state = self.states[trans["new_state"]]

            # Check if max transitions reached
            if self.numTransitions >= self.maxTransitions:
                print("Rejected")
                break

    def __repr__(self):
        s = ""
        for state in self.states:
            s += f'{self.states[state]}\n'
        return s


def createTuringMachine():
    tm = TuringMachine()



    with open('doublea.txt', 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip()
            line = line.split(", ")

            if len(line) == 1:
                tm.add_state(State(line[0]))
            else:
                # new State
                state = tm.getState(line[0])

                if state == None:
                    state = State(line[0])

                # check new state in turing, if not add it
                if tm.hasState(line[4]) == False:
                    tm.add_state(State(line[4]))

                # old symbol, new symbol, direction, new state
                state.add_transition(line[1], line[2], line[3], line[4])
                tm.add_state(state)
    return tm





if __name__ == "__main__":
    tm = createTuringMachine()
    print(tm)
    tm.run("_bbabbbaa")
