import Automaton
from RegexToNfa import regex_to_nfa
from RemoveE import remove_e
from BuildPdka import build_pdka
from BuildMpdka import build_mpdka
import json

def test_build_mpdka():
    nfa = regex_to_nfa("(e | (a|b)*b)b(a|b)*")
    remove_e(nfa)
    pdka = build_pdka(nfa)
    mpdka = build_mpdka(pdka)
    data = {"s0": 0, "states": [0, 1, 2], "final": [1, 1, 1, 1], "delta": [{"from": 0, "to": 1, "sym": "b"}, {"from": 0, "to": 2, "sym": "a"}, {"from": 1, "to": 1, "sym": "b"}, {"from": 1, "to": 1, "sym": "a"}, {"from": 2, "to": 0, "sym": "b"}, {"from": 2, "to": 2, "sym": "a"}]}
    json_string = json.dumps(data)
    assert mpdka.to_json() == json_string
    
    nfa = regex_to_nfa("(((e | e)*)+ | ((e*)*(e+)+)*)*")
    remove_e(nfa)
    pdka = build_pdka(nfa)
    mpdka = build_mpdka(pdka)
    data = {"s0": 0, "states": [0], "final": [0], "delta": []}
    json_string = json.dumps(data)
    assert mpdka.to_json() == json_string