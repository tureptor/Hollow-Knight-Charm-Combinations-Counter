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
            for i, row in enumerate(charmRows, 1):
                name, notches = row[0], int(row[1])
                self.charmNotches[i] = notches
                self.charmName[i] = name

    def getCharmName(self, id):
        return self.charmName[id]

    def hasConflict(self, combo):
        if {24, 36}.issubset(combo):  # combo has both grimmchild and carefree
            return True
        if {1, 42}.issubset(combo):  # combo has both kingsoul and voidheart
            return True
        return False

    def listCombos(self):
        numCharms = len(self.charmNotches)
        maxNotchesToConsider = self.numNotches
        if self.allowOvercharmed:
            maxNotchesToConsider += max(self.charmNotches.values()) - 1

        partialCombos = []
        # partialCombos[i][n] contains a list of combinations
        # the combinations themselves are a list of ints corresponding to the charm id
        # These combinations use exactly n notches
        # The notches within the combinations have an id <= i

        for i in range(numCharms + 1):
            partialCombos.append([[] for n in range(maxNotchesToConsider + 1)])

        partialCombos[0][0].append([])
        # If we have no notches and no charms available, we can always use the empty set
        # The algorithm will build all other combinations based off this initial entry.

        # remove miniters=1 parameter if not using the tqdm version of itertools
        for i, n in itertools.product(
            range(1, numCharms + 1), range(0, maxNotchesToConsider + 1), miniters=1
        ):
            charmN = self.charmNotches[i]
            partialCombos[i][n] += [c for c in partialCombos[i - 1][n]]
            if (charmN + n <= self.numNotches) or (
                self.allowOvercharmed and n < self.numNotches
            ):
                for prev in partialCombos[i - 1][n]:
                    partialCombos[i][n + charmN].append(prev + [i])

        print("finished generation of combos")
        for w in partialCombos[numCharms]:
            for combo in w:
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
