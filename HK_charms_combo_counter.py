###########################################################
# Original version written 2024-02-14 by Spencer Trumbore #
# Rewritten 2024-05-04 by Mansoor Amiri                   #
###########################################################

import csv
from tqdm.contrib import itertools

# replace with just `import itertools` if you don't want tqdm


class CharmComboFinder:
    def __init__(self, numNotches, allowOvercharmed=False):
        self.charmNotches = dict()  # int (id) => int (notches used by charm)
        self.charmName = dict()  # int (id) => str (charm name)
        self.numNotches = numNotches
        self.allowOvercharmed = allowOvercharmed

        with open("hk_charms.csv", "r") as rawData:
            charmRows = csv.reader(rawData, delimiter=",")
            for row in charmRows:
                id, name, notches = int(row[0]), row[1], int(row[2])
                self.charmNotches[id] = notches
                self.charmName[id] = name

    def getCharmName(self, id):
        return self.charmName[id]

    def hasConflict(self, combo):
        if {39, 40}.issubset(combo):  # combo has both grimmchild and carefree
            return True
        if {41, 42}.issubset(combo):  # combo has both kingsoul and voidheart
            return True
        return False

    def listCombos(self):
        numCharms = len(self.charmNotches)
        maxNotchesToConsider = self.numNotches
        if self.allowOvercharmed:
            maxNotchesToConsider += max(self.charmNotches.values()) - 1

        partialCombos = []
        # partialCombos[i][n] contains a list of tuples
        # Each tuple is composed of a combination and a number
        # These combinations use exactly n notches
        # The notches within the combinations have an id <= i
        # The number is the max number of notches used by a single charm
        # This is used for determining overcharmed combinations.

        for i in range(numCharms + 1):
            partialCombos.append([[] for n in range(maxNotchesToConsider + 1)])

        partialCombos[0][0].append(([], 0))
        # If we have no notches and no charms available, we can always use the empty set
        # The algorithm will build all other combinations based off this initial entry.

        # remove miniters=1 parameter if not using the tqdm version of itertools
        for i, n in itertools.product(
            range(1, numCharms + 1), range(0, maxNotchesToConsider + 1), miniters=1
        ):
            charmN = self.charmNotches[i]
            partialCombos[i][n] += [c for c in partialCombos[i - 1][n]]
            if charmN + n <= self.numNotches:
                for prev in partialCombos[i - 1][n]:
                    partialCombos[i][n + charmN].append(
                        (prev[0] + [i], max(prev[1], charmN))
                    )
            elif self.allowOvercharmed:
                for prev in partialCombos[i - 1][n]:
                    if n < self.numNotches or n + charmN - prev[1] < self.numNotches:
                        # either there is an empty notch in the existing combination
                        # or we can take the biggest charm out (-prev[1]), put the current charm in (+charmN)
                        # and this would leave empty notches for the biggest charm to put back in
                        partialCombos[i][n + charmN].append(
                            (prev[0] + [i], max(prev[1], charmN))
                        )

        print("finished generation of combos")
        for w in partialCombos[numCharms]:
            for combo, _ in w:
                if not self.hasConflict(combo):
                    yield combo


a = CharmComboFinder(numNotches=11, allowOvercharmed=True)

with open("combos.txt", "w") as outputFile:
    for i, combo in enumerate(a.listCombos()):
        if i % 2**13 == 0:
            print("Lines written:", i + 1, end="\r")
        outputFile.write(
            str(i + 1)
            + "\t"
            + ", ".join(a.getCharmName(charm) for charm in combo)
            + "\n"
        )
        # alternative encoding:
        # outputFile.write(",".join(str(charm) for charm in combo) + "\n")
    print("Lines written:", i + 1)  # i % 2**13 != 0 otherwise print() would suffice

print("done")
