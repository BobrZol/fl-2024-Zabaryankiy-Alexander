import Automaton
import State


def find_equiv(pdka, equiv_class):
    alphabet = pdka.get_alphabet()
    array = [[0 for _ in range(len(pdka.arr_states))] for _ in range(len(alphabet))]

    for i in range(len(pdka.arr_states)):
        for j in range(len(alphabet)):
            ngh = pdka.arr_states[i].transitions[alphabet[j]][0]
            array[j][i] = equiv_class[pdka.get_state_ind(ngh)]

    bl = {}
    ind = 0
    new_equiv_class = [0 for _ in range(len(pdka.arr_states))]
    for i in range(len(pdka.arr_states)):
        equiv = [equiv_class[i]]
        for j in range(len(alphabet)):
            equiv.append(array[j][i])
        if tuple(equiv) not in bl:
            bl[tuple(equiv)] = ind
            new_equiv_class[i] = ind
            ind += 1
        else:
            new_equiv_class[i] = bl[tuple(equiv)]

    if new_equiv_class == equiv_class:
        return new_equiv_class, array
    return find_equiv(pdka, new_equiv_class)


def build_mpdka(pdka):
    alphabet = pdka.get_alphabet()
    equiv_class = [0 for _ in range(len(pdka.arr_states))]

    ind = 0
    for st in pdka.arr_states:
        if st in pdka.final_states:
            equiv_class[ind] = 1
        ind += 1

    new_equiv_class, array = find_equiv(pdka, equiv_class)


    num = 0
    for item in new_equiv_class:
        num = max(num, item)

    mpdka = Automaton.Automaton()
    mpdka.final_states = []

    for i in range(num):
        new_st = State.State()
        mpdka.arr_states.append(new_st)

    for i in range(len(pdka.arr_states)):
        start = mpdka.arr_states[new_equiv_class[i]]
        if equiv_class[i] == 1:
            mpdka.final_states.append(start)
        for j in range(len(alphabet)):
            to = mpdka.arr_states[array[j][i]]
            if (alphabet[j] not in start.transitions) or (
                to not in start.transitions[alphabet[j]]
            ):
                mpdka.add_transition(start, alphabet[j], to)
    mpdka.rm_unused_states()
    return mpdka
