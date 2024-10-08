import Automaton
from step1 import regex_to_nfa
from step2 import remove_e
from step3 import build_pdka
from step4 import build_mpdka


def main():
    # nfa = regex_to_nfa("a (a(ab)*a(ab)* | b)*")
    nfa = regex_to_nfa("(e | (a|b)*b)b(a|b)*")
    # nfa = regex_to_nfa("a (a(ab)* | b)*")
    # nfa.get_info()
    remove_e(nfa)
    # nfa.get_info()
    pdka = build_pdka(nfa)
    # pdka.get_info()
    mpdka = build_mpdka(pdka)
    mpdka.get_info()


if __name__ == "__main__":
    main()
