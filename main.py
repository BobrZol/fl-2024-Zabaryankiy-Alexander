import Automaton
from RegexToNfa import regex_to_nfa
from RemoveE import remove_e
from BuildPdka import build_pdka
from BuildMpdka import build_mpdka
from Test import test_build_mpdka


def main():
    test_build_mpdka()
    nfa = regex_to_nfa("(aa(a|ba)*bb(ab)*)*")
    #nfa = regex_to_nfa("ab")
    #nfa.get_info()
    remove_e(nfa)
    # nfa.get_info()
    pdka = build_pdka(nfa)
    #pdka.get_info()
    mpdka = build_mpdka(pdka)
    mpdka.get_info()


if __name__ == "__main__":
    main()
