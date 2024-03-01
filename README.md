# About

## How Many Charm Combinations Are There In Hollow Knight?

Without exceeding 11 charm notches and being "overcharmed", there are **4,460,494** combinations of charms possible in *Hollow Knight*. I wrote this quick-and-dirty program to enumerate them. This solution is suboptimal, but only takes about 3 minutes to run as it is now. The resulting text file, combos.txt, is about 800mb. I may modify this in the future to make it run faster and to accommodate "overcharmed" combinations (combinations exceeding 11 notches). I invite others to try to calculate those combinations before I do.

## Rules

 - There are 45 charms in the game and up to 11 notches to hold them. Different charms have different notch costs (or "weights"). For the purposes of this project, it is simpler to consider these three pairs as single charms, bringing the total number of charms down to 42.
     - The following 3 pairs of charms are counted as distinct, but they cannot coexist because they are upgrades:
	     - **Fragile Heart** &rarr; **Unbreakable Heart**
	     - **Fragile Greed** &rarr; **Unbreakable Greed**
    	 - **Fragile Strength** &rarr; **Unbreakable Strength**
- The following two pairs of charms cannot coexist because they require different choices during a playthrough. Grimmchild has multiple upgrade stages, but they are not considered unique by any wikis:
	- **Grimmchild I-IV**, **Carefree Melody**
- **Kingsoul** and **Voidheart** are also an upgrade pair that cannot coexist.
