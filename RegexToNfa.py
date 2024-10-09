import Automaton
import State


def outer_brackets(regex):
    if len(regex) < 2:
        return False
    tmp = 0
    ind = 0
    for cr in regex:
        if cr == "(":
            tmp += 1
        if cr == ")":
            tmp -= 1
        if tmp == 0 and ind < len(regex) - 1:
            return False
        ind += 1
    return True


def regex_to_nfa(regex):
    regex = regex.replace(" ", "")
    # print("regex_to_nfa " + regex)
    if outer_brackets(regex):
        regex = regex[1 : len(regex) - 1]

    if len(regex) == 1:
        return Automaton.Automaton(regex)
    if (
        regex[len(regex) - 1] == "*" or regex[len(regex) - 1] == "+"
    ) and outer_brackets(regex[0 : len(regex) - 1]):
        return build_nfa(regex_to_nfa(regex[0 : len(regex) - 1]), regex[len(regex) - 1])

    if len(regex) == 3 and regex[1] in ['|', ''] and regex[0].isalpha() and regex[2].isalpha():
        return merge_nfa(regex_to_nfa(regex[0]), regex_to_nfa(regex[2]), regex[1])
    if len(regex) == 2 and regex[0].isalpha() and regex[1] in ['*', '+']:
        return build_nfa(regex_to_nfa(regex[0]), regex[1])
    if len(regex) == 2 and regex[0].isalpha() and regex[1].isalpha():
        return merge_nfa(regex_to_nfa(regex[0]), regex_to_nfa(regex[1]), "")

    ind = 0
    tmp = 0
    for cr in regex:
        if cr == "(":
            tmp += 1
        if cr == ")":
            tmp -= 1
        if tmp == 0 and ind + 1 < len(regex):
            # print("ind", ind, "rgx", regex[0:ind + 1], "cr", cr)
            if regex[ind + 1] == "|":
                return merge_nfa(
                    regex_to_nfa(regex[0:ind + 1]),
                    regex_to_nfa(regex[ind + 2 :]),
                    regex[ind + 1],
                )
            elif regex[ind + 1] != "*" and regex[ind + 1] != "+":
                return merge_nfa(
                    regex_to_nfa(regex[0:ind + 1]), regex_to_nfa(regex[ind + 1: ]), ""
                )
        ind += 1


def build_nfa(nfa, str_opr):
    start = State.State()
    finish = State.State()

    nfa.arr_states.append(start)
    nfa.arr_states.append(finish)

    nfa.add_transition(nfa.final_states[0], "e", nfa.start_state)

    nfa.add_transition(nfa.final_states[0], "e", finish)
    nfa.add_transition(start, "e", nfa.start_state)

    nfa.final_states[0] = finish
    nfa.start_state = start
    if str_opr == "*":
        nfa.add_transition(start, "e", finish)
    
    return nfa


def merge_nfa(nfa1, nfa2, str_opr):
    nfa = Automaton.Automaton()
    nfa.arr_states.extend(nfa1.arr_states)
    nfa.arr_states.extend(nfa2.arr_states)
    if str_opr == "|":
        nfa.add_transition(nfa.final_states[0], "e", nfa1.start_state)
        nfa.add_transition(nfa.final_states[0], "e", nfa2.start_state)

        state = State.State()
        nfa.add_state(state)

        nfa.final_states[0] = state
        nfa.add_transition(nfa1.final_states[0], "e", nfa.final_states[0])
        nfa.add_transition(nfa2.final_states[0], "e", nfa.final_states[0])
    if str_opr == "":
        finish = State.State()
        nfa.arr_states.append(finish)

        nfa.add_transition(nfa.start_state, "e", nfa1.start_state)
        nfa.add_transition(nfa1.final_states[0], "e", nfa2.start_state)
        nfa.add_transition(nfa2.final_states[0], "e", finish)

        nfa.final_states[0] = finish
    return nfa
