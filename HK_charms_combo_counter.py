###########################################################
# Original version written 2024-02-14 by Spencer Trumbore #
# Rewritten 2024-05-04 by Mansoor Amiri                   #
###########################################################

import csv
from typing import Generator

type CharmID = int
type Combination = list[CharmID]

try:
    from tqdm import tqdm

except ImportError:

    def tqdm(iterable, **kwargs):
        return iterable


class CharmComboFinder:
    def __init__(self, numNotches: int, allowOvercharmed: bool = False):
        self.charmNotches: list[int] = [0]
        self.charmName: dict[CharmID, str] = dict()

        self.numNotches: int = numNotches
        self.allowOvercharmed: bool = allowOvercharmed

        with open("hk_charms.csv", "r") as rawData:
            charmRows = csv.reader(rawData, delimiter=",")
            for i, row in enumerate(charmRows, 1):
                name, notches = row[0], int(row[1])
                self.charmNotches.append(notches)
                self.charmName[i] = name

    def getCharmName(self, id: CharmID) -> str:
        return self.charmName[id]

    def causesConflict(self, i: CharmID, combo: Combination) -> bool:
        return (i == 36 and 24 in combo) or (i == 42 and 1 in combo)

    def getCombosGenerator(self) -> Generator[Combination, None, None]:
        numCharms: int = len(self.charmName)
        maxNotchesToConsider: int = self.numNotches
        if self.allowOvercharmed:
            maxNotchesToConsider += max(self.charmNotches) - 1

        partialCombos: list[list[list[Combination]]] = []
        # partialCombos[i][n] contains a list of combinations
        # These combinations use exactly n notches
        # The notches within the combinations have an id <= i

        for i in range(numCharms + 1):
            partialCombos.append([[] for _ in range(maxNotchesToConsider + 1)])

        partialCombos[0][0].append([])
        # If we have no notches and no charms available, we can always use the empty set
        # The algorithm will build all other combinations based off this initial entry.

        # remove miniters=1 parameter if not using the tqdm version of itertools
        for i in tqdm(
            range(1, numCharms + 1), miniters=1, desc="Generating combinations"
        ):
            for n in tqdm(
                range(maxNotchesToConsider + 1),
                leave=False,
                miniters=1,
                desc=f"Considering varying notch counts",
            ):
                charmN: int = self.charmNotches[i]
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

        return (combo for w in partialCombos[numCharms] for combo in w)


with open("combos.txt", "w") as outputFile:
    a = CharmComboFinder(numNotches=11, allowOvercharmed=False)
    comboGen = a.getCombosGenerator()
    outputFile.writelines(
        str(i) + "\t" + ", ".join(a.getCharmName(charm) for charm in combo) + "\n"
        for i, combo in enumerate(
            tqdm(comboGen, desc="Writing output to file", unit=" lines"), 1
        )
    )
    # alternative encoding:
    # outputFile.write(",".join(str(charm) for charm in combo) + "\n")

print("done")
