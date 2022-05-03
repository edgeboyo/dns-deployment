import random

alphabet = [chr(ord('a') + i) for i in range(ord('z') - ord('a') + 1)]


def cutAndPlace(word, location, newChar):
    joiner = [word[:location], newChar, word[location:]]

    return "".join(joiner)


def emplace(word, location, newChar):
    joiner = [word[:location], newChar, word[location+1:]]

    return "".join(joiner)


def selectNonPeriods(url):
    valid = []

    validSection = []
    for i, c in enumerate(url):
        if c != '.':
            validSection.append(i)
        else:
            valid = valid + validSection
            validSection = []

    return valid


def derive(selected):
    method = random.randrange(3)

    validPositions = selectNonPeriods(selected)
    if method == 0:  # change letter to a random new one
        pos = random.choice(validPositions)
        c = selected[pos]

        alph = alphabet.copy()
        alph.remove(c)

        selected = emplace(selected, pos, random.choice(alph))
    elif method == 1:  # copy letter and add it right after
        pos = random.choice(validPositions)
        c = selected[pos]

        selected = cutAndPlace(selected, pos, c)

    elif method == 2:  # add random letter right after
        pos = random.choice(validPositions)
        c = selected[pos]

        alph = alphabet.copy()
        alph.remove(c)

        selected = cutAndPlace(selected, pos, random.choice(alph))

    return selected


def createDerivations(initial, stopAt=100, failLock=10):
    derivations = [initial]

    failed = 0
    while len(derivations) < stopAt or failed > failLock:
        newWord = derive(random.choice(derivations))

        if newWord in derivations:
            failed += 1
            continue

        derivations.append(newWord)
        failed = 0

    if len(derivations) != stopAt:
        print("Generation hit the failure lock. Generated %d derivations" %
              len(derivations))

    return derivations
