###########################################################
# Original version written 2024-02-14 by Spencer Trumbore #
# Rewritten 2024-05-04 by Mansoor Amiri                   #
###########################################################

from csv import reader
from typing import Iterator
from argparse import ArgumentParser
import gzip


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
        self.charmNames: list[str] = [""]
        self.finalCombos: list[list[Combination]] = []

        self.numNotches: int = numNotches
        self.allowOvercharmed: bool = allowOvercharmed

        with open("hk_charms.csv", "r") as rawData:
            charmRows = reader(rawData, delimiter=",")
            for i, row in enumerate(charmRows, 1):
                name, notches = row[0], int(row[1])
                self.charmNotches.append(notches)
                self.charmNames.append(name)

    def getCharmName(self, id: CharmID) -> str:
        return self.charmNames[id]

    def causesConflict(self, i: CharmID, combo: Combination) -> bool:
        return (i == 36 and 24 in combo) or (i == 42 and 1 in combo)

    def genCombos(self):
        numCharms: int = len(self.charmNames) - 1
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
        self.finalCombos = partialCombos[numCharms]

    def getCombosGenerator(self) -> Iterator[Combination]:
        if not self.finalCombos:
            self.genCombos()
        return (combo for w in self.finalCombos for combo in w)


def encodeLine(
    i: int, combo: Combination, alt: bool, charmNames: list[str] = []
) -> str:
    if alt:
        return ",".join(str(charm) for charm in combo) + "\n"
    else:
        return str(i) + "\t" + ", ".join(charmNames[id] for id in combo) + "\n"


def main():
    parser = genArgParser()
    args = parser.parse_args()

    finderObj = CharmComboFinder(
        numNotches=args.notches, allowOvercharmed=args.overcharmed
    )
    comboGen = finderObj.getCombosGenerator

    count = sum(
        1 for _ in tqdm(comboGen(), desc="Counting combos", unit=" combos", leave=False)
    )
    print(f"Total {count=}")

    if args.no_file:
        return

    if args.compress:
        outputFile = gzip.open(args.filename + ".gz", "wt", compresslevel=1)
    else:
        outputFile = open(args.filename, "w")

    outputFile.writelines(
        encodeLine(i, combo, args.altencode, finderObj.charmNames)
        for i, combo in enumerate(
            tqdm(comboGen(), desc="Writing combos to file", unit=" lines", total=count),
            1,
        )  # type: ignore
    )
    outputFile.close()


def genArgParser():
    parser = ArgumentParser(prog="HK charms combination counter")
    parser.add_argument(
        "-n",
        "--notches",
        default=11,
        type=int,
        help="max number of notches allowed (default: 11)",
    )
    parser.add_argument(
        "-o",
        "--overcharmed",
        action="store_true",
        help="allow overcharmed combinations (default: no)",
    )
    parser.add_argument(
        "-f",
        "--filename",
        default="combos.txt",
        help="the filename to write to. If --compress is used, then .gz is automatically appended. (default: combos.txt)",
    )
    parser.add_argument(
        "-c",
        "--compress",
        action="store_true",
        help="compress output with gzip before writing to file. Greatly reduces file size at the cost of some CPU overhead (default: no)",
    )
    parser.add_argument(
        "-a",
        "--altencode",
        action="store_true",
        help="alternative encoding with numbers corresponding to lines in the csv file instead of charm names. Reduces file size significantly (default: no)",
    )
    parser.add_argument(
        "--no-file",
        action="store_true",
        help="only print the count, and do not write to a file (default: do write to file)",
    )
    return parser


main()
print("done")
