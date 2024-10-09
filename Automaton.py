import State
import json


class Automaton:
    def __init__(self, str_=""):
        self.start_state = State.State()
        if str_ == "":
            self.arr_states = [self.start_state]
            self.final_states = [self.start_state]
        else:
            new_state = State.State()
            self.add_transition(self.start_state, str_, new_state)
            self.arr_states = [self.start_state, new_state]
            self.final_states = [new_state]

    def to_json(self):
        data = {}
        data["s0"] = self.get_state_ind(self.start_state)
        data["states"] = list(map(self.get_state_ind, self.arr_states))
        data["final"] = list(map(self.get_state_ind, self.final_states))
        data["delta"] = []

        for state in self.arr_states:
            for key in state.transitions.keys():
                for val in state.transitions[key]:
                    data["delta"].append(
                        {
                            "from": self.get_state_ind(state),
                            "to": self.get_state_ind(val),
                            "sym": key,
                        }
                    )
        json_string = json.dumps(data)
        return json_string

    def get_alphabet(self):
        alphabet = []
        for st in self.arr_states:
            for alph in st.transitions.keys():
                if alph not in alphabet:
                    alphabet.append(alph)
        return alphabet

    def get_state_ind(self, state):
        ind = 0
        for st in self.arr_states:
            if st == state:
                return ind
            ind += 1
        return -1

    def get_info(self):
        print(len(self.arr_states))
        ind = 0
        for state in self.arr_states:
            print("State " + str(ind) + ":")
            ind += 1
            if self.start_state == state:
                print("is start_state")
            if state in self.final_states:
                print("is final_states")

            for key in state.transitions.keys():
                for val in state.transitions[key]:
                    print("to " + str(self.get_state_ind(val)) + " by " + key)
            print()

    def add_state(self, state):
        self.arr_states.append(state)

    def add_transition(self, from_state, symbol, to_state):
        if symbol not in from_state.transitions:
            from_state.transitions[symbol] = []
        from_state.transitions[symbol].append(to_state)

    def rm_unused_states(self):
        rm_list = []
        for st1 in self.arr_states:
            if st1 == self.start_state:
                continue
            num_tr_in = 0
            num_tr_out = 0
            for st2 in self.arr_states:
                if st1 in sum(list(st2.transitions.values()), []) and st1 != st2:
                    num_tr_in += 1
                if st2 in sum(list(st1.transitions.values()), []) and st1 != st2:
                    num_tr_out += 1
            if num_tr_in == 0 or (num_tr_out == 0 and st1 not in self.final_states):
                rm_list.append(st1)

        for st in rm_list:
            if st in self.final_states:
                self.final_states.remove(st)
            for state in self.arr_states:
                rm_list_state = []
                for key in state.transitions.keys():
                    for val in state.transitions[key]:
                        if val == st:
                            rm_list_state.append(key)
                for rm in rm_list_state:
                    state.transitions[rm].remove(st)
            self.arr_states.remove(st)
