def foo(nfa, state, path):
    cp_list = state.transitions.copy()
    for key in cp_list.keys():
        for ngh in cp_list[key]:
            if key == "e":
                if ngh in path:
                    continue
                path_copy = path.copy()
                path_copy.append(state)
                for st in path_copy:
                    if ngh in nfa.final_states:
                        nfa.final_states.append(st)
                foo(nfa, ngh, path_copy)
            else:
                for st in path:
                    if (key not in st.transitions) or (ngh not in st.transitions[key]):
                        nfa.add_transition(st, key, ngh)


def remove_e(nfa):
    for st in nfa.arr_states:
        foo(nfa, st, [])

    for st in nfa.arr_states:
        new_list = {}

        for key in st.transitions.keys():
            for ngh in st.transitions[key]:
                if key != "e":
                    if key not in new_list:
                        new_list[key] = []
                    new_list[key].append(ngh)

        st.transitions = new_list
    nfa.rm_unused_states()
