import os
from pathlib import Path
from collections import Counter


CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PATH = Path(CUR_DIR) / ".." / "input" / "sample_input.txt"
WORD = 'PUMPKIN'


def split_into_syllables(word, *midpoints):
    start = 0
    syllables = []
    for midpoint in midpoints:
        part = word[start:midpoint]
        start += midpoint
        syllables.append(part)
    rest = word[len("".join(syllables)):]
    if rest:
        syllables.append(rest)
    return syllables


SYLLABLES = split_into_syllables(WORD, 4)


def get_lines():
    with open(PATH) as f:
        for line in f:
            yield line


def has_all_letters(line, word):
    counter = Counter(word)
    flag = "".join(c for c in line if c in counter) == word
    if flag:
        indices = [line.index(c) for c in counter.keys()]
        flag &= not any(i + 1 in indices for i in indices)
    return flag


def get_all_positions(line, word):
    positions = []
    start = 0
    while (pos := line.find(word, start)) != -1:
        positions.append(pos)
        start = pos + len(word)
    return positions


def is_glued_position(position, line, word):
    try:
        assert word in line
        assert len(line) > len(word)
    except AssertionError:
        return False
    result = False
    before = position - 1
    after = position + len(word)
    if before >= 0 and line[before] in word:
        result = True
    elif after < len(line) and line[after] in word:
        result = True
    return result


def discard(positions, line, word):
    to_be_removed = 0
    beg_pos = 0
    if beg_pos in positions:
        positions.remove(beg_pos)
        to_be_removed += 1
    end_pos = len(line) - len(word)
    if end_pos in positions:
        positions.remove(end_pos)
        to_be_removed += 1
    return to_be_removed


def check_across_lines(current, after, syllables):
    assert len(syllables) == 2
    return (
        current.rstrip().endswith(syllables[0])
        and after.lstrip().startswith(syllables[1])
    )


# algorithm
def get_matches(prev, line, word, syllables):
    # check potential candidates
    positions = get_all_positions(line, word)
    candidates = len(positions)
    # if not zero - discard all glued
    if candidates > 0:
        for pos in positions:
            if is_glued_position(pos, line, word):
                candidates -= 1
    if candidates > 0:
        # if not zero - discard where is at beginning or end
        to_be_removed = discard(positions, line, word)
        candidates -= to_be_removed
    # if zero check across lines
    if prev and check_across_lines(prev, line, syllables):
        candidates += 1
    # count positions of reversed
    candidates += len(get_all_positions(line, word[::-1]))
    # if still zero match - try all letters
    if candidates == 0 and has_all_letters(line, word):
        candidates += 1
    return candidates


def main():
    word_count = 0
    prev = None
    for idx, line in enumerate(get_lines()):
        matches = get_matches(prev, line, WORD, SYLLABLES)
        # if matches > 0:
        #     print(idx+1, matches, line, end='')
        # print(idx + 1, line, end='')
        word_count += matches
        prev = line
    print(word_count)
    # result: 52 (if word letters should be apart at least 1 other character) / 60


if __name__ == '__main__':
    main()