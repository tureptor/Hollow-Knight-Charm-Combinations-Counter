###########################################################
# Original version written 2024-02-14 by Spencer Trumbore #
# Rewritten 2024-05-04 by Mansoor Amiri                   #
###########################################################

import csv
from tqdm import trange, tqdm


class CharmComboFinder:
    def __init__(self, numNotches, allowOvercharmed=False):
        self.charmNotches = dict()  # int (id) => int (notches used by charm)
        self.charmName = dict()  # int (id) => str (charm name)
        self.finalCombos = []

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

    def causesConflict(self, i, combo):
        return (i == 36 and 24 in combo) or (i == 42 and 1 in combo)

    def genCombos(self):
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
        for i in trange(1, numCharms + 1, miniters=1):
            for n in trange(0, maxNotchesToConsider + 1, leave=False, miniters=1):
                charmN = self.charmNotches[i]
                partialCombos[i][n] += partialCombos[i - 1][n]
                if (charmN + n <= self.numNotches) or (
                    self.allowOvercharmed and n < self.numNotches
                ):
                    for prev in partialCombos[i - 1][n]:
                        if self.causesConflict(i, prev):
                            continue
                        partialCombos[i][n + charmN].append(prev + [i])
            partialCombos[i - 1] = []
            # we will never need this row again - we just generated partialCombos[i]
            # which is the only row the next (i+1th) iteration will use

        print("finished generation of combos")
        self.finalCombos = (combo for w in partialCombos[numCharms] for combo in w)

    def yieldCombos(self):
        return self.finalCombos


with open("combos.txt", "w") as outputFile:
    a = CharmComboFinder(numNotches=11, allowOvercharmed=True)
    a.genCombos()
    outputFile.writelines(
        str(i) + "\t" + ", ".join(a.getCharmName(charm) for charm in combo) + "\n"
        for i, combo in enumerate(tqdm(a.yieldCombos(), desc="Lines written"), 1)
    )
    # alternative encoding:
    # outputFile.write(",".join(str(charm) for charm in combo) + "\n")

print("done")
