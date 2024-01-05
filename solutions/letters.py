import os
import random
import time
from collections import defaultdict
from pathlib import Path
from pprint import pp


CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PATH = Path(CUR_DIR) / ".." / "input" / "letter_game.txt"


def naive_without_duplicates(transitions):
    initial = random.choice(list(transitions.keys()))
    sequence = [initial]
    used = {initial}
    def get_moves(key, transitions):
        if values := transitions.get(key):
            possible_picks = set(values)
            possible_picks -= used
            return list(possible_picks)
        return []
    def recur(key, transitions, sequence):
        moves = get_moves(key, transitions)
        if len(moves) > 0:
            pick = random.choice(moves)
            transitions[key].remove(pick)
            sequence.append(pick)
            used.add(pick)
            return recur(pick, transitions, sequence)
        else:
            return " - ".join(sequence)
    return recur(initial, transitions, sequence)


def naive(transitions):
    initial = random.choice(list(transitions.keys()))
    sequence = [initial]
    def has_move(key, transitions):
        return len(transitions.get(key, [])) > 0
    def do_move(key, transitions):
        return random.choice(transitions[key])
    def recur(key, transitions, sequence):
        if has_move(key, transitions):
            pick = do_move(key, transitions)
            transitions[key].remove(pick)
            sequence.append(pick)
            return recur(pick, transitions, sequence)
        else:
            return " - ".join(sequence)
    return recur(initial, transitions, sequence)


def main():
    with open(PATH) as f:
        names = list(set(line.strip() for line in f))
        transitions = defaultdict(list)
        for name in names:
            others = names.copy()
            others.remove(name)
            for other in others:
                if name[-1] == other[0]:
                    transitions[name].append(other)
    possible_transitions = sum([len(names) for names in transitions.values()])
    print(f"Possible transitions: {possible_transitions}")
    d = {}
    start = time.time()
    while True:
        try:
            result =  naive_without_duplicates(transitions)
            length = result.count(" - ") + 1
            if length not in d:
                print(f"Found new sequence: {length}")
            d[length] = result
            if time.time() - start > 1:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            print()
            n = max(list(d.keys()))
            print(f"Sequence length: {n}")
            print(d.get(n))
            exit()


if __name__ == '__main__':
    main()