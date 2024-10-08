import Automaton
import State


def outer_brackets(regex):
    tmp = 0
    ind = 0
    outer_brackets = True
    for cr in regex:
        if cr == "(":
            tmp += 1
        if cr == ")":
            tmp -= 1
        if tmp == 0 and ind < len(regex) - 1:
            outer_brackets = False
        ind += 1
    return outer_brackets


def regex_to_nfa(regex):
    regex = regex.replace(" ", "")
    # print("regex_to_nfa " + regex)

    if len(regex) == 1:
        return Automaton.Automaton(regex)
    if (
        regex[len(regex) - 1] == "*" or regex[len(regex) - 1] == "+"
    ) and outer_brackets(regex[0 : len(regex) - 1]):
        return build_nfa(regex_to_nfa(regex[0 : len(regex) - 1]), regex[len(regex) - 1])

    if outer_brackets(regex):
        regex = regex[1 : len(regex) - 1]

    if len(regex) == 3:
        return merge_nfa(regex_to_nfa(regex[0]), regex_to_nfa(regex[2]), regex[1])
    if len(regex) == 2:
        return merge_nfa(regex_to_nfa(regex[0]), regex_to_nfa(regex[1]), "")

    ind = 0
    tmp = 0
    for cr in regex:
        ind += 1
        if cr == "(":
            tmp += 1
        if cr == ")":
            tmp -= 1
        if tmp == 0:
            # print("opr", regex[ind], "ind", ind)
            if regex[ind] == "|":
                return merge_nfa(
                    regex_to_nfa(regex[0:ind]),
                    regex_to_nfa(regex[ind + 1 :]),
                    regex[ind],
                )
            elif regex[ind] != "*" and regex[ind] != "+":
                return merge_nfa(
                    regex_to_nfa(regex[0:ind]), regex_to_nfa(regex[ind:]), ""
                )


def build_nfa(nfa, str_opr):
    nfa.add_transition(nfa.final_states[0], "e", nfa.start_state)
    if str_opr == "*":
        nfa.add_transition(nfa.start_state, "e", nfa.final_states[0])
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
        nfa.add_transition(nfa.start_state, "e", nfa1.start_state)
        nfa.add_transition(nfa1.final_states[0], "e", nfa2.start_state)

        nfa.final_states[0] = nfa2.final_states[0]
    return nfa
