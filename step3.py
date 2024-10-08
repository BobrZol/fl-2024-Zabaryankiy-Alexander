import Automaton
import State


def build_pdka(nfa):
    p_queue = [[nfa.start_state]]
    pdka_q = [[nfa.start_state]]
    alphabet = nfa.get_alphabet()

    while len(p_queue) > 0:
        # print("dka_q")
        # for arr in dka_q:
        #   transformed_array = map(nfa.get_state_ind, arr)
        #   print(' '.join(map(str, transformed_array)))

        curr_state = p_queue[0]
        # transformed_array = map(nfa.get_state_ind, curr_state)
        # print("curr_state " + ' '.join(map(str, transformed_array)))
        del p_queue[0]

        for alph in alphabet:
            new_state = []
            for st in curr_state:
                for alph_in_curr in st.transitions.keys():
                    if alph_in_curr == alph:
                        new_state.extend(st.transitions[alph_in_curr])
            if set(new_state) not in map(set, pdka_q) and new_state != []:
                p_queue.append(new_state)
                pdka_q.append(new_state)

    # print("pdka_q")
    # for arr in pdka_q:
    #   transformed_array = map(nfa.get_state_ind, arr)
    #   print(' '.join(map(str, transformed_array)))

    # pdka
    pdka = Automaton.Automaton()
    pdka.final_states = []

    for i in range(len(pdka_q) - 1):
        new_st = State.State()
        pdka.arr_states.append(new_st)

    drain = State.State()
    bl_drain = False

    for i in range(len(pdka_q)):
        curr_state = pdka_q[i]
        for alph in alphabet:
            to_state = []
            for st in curr_state:
                # if st == nfa.start_state:
                #   print("YESSS")
                #   pdka.start_state = curr_state
                if st in nfa.final_states:
                    pdka.final_states.append(pdka.arr_states[i])
                for alph_in_curr in st.transitions.keys():
                    if alph_in_curr == alph:
                        to_state.extend(st.transitions[alph_in_curr])

            if to_state == []:
                # transformed_array = map(nfa.get_state_ind, curr_state)
                # print("curr_state " + str(i) + ' ' + ' '.join(map(str, transformed_array)))
                bl_drain = True
                pdka.add_transition(pdka.arr_states[i], alph, drain)
                continue

            transformed_array = map(nfa.get_state_ind, to_state)

            for j in range(len(pdka_q)):
                transformed_array = map(nfa.get_state_ind, pdka_q[j])
                if set(to_state) == set(pdka_q[j]):
                    pdka.add_transition(pdka.arr_states[i], alph, pdka.arr_states[j])

    if bl_drain:
        for alph in alphabet:
            pdka.add_transition(drain, alph, drain)
        pdka.arr_states.append(drain)

    return pdka
