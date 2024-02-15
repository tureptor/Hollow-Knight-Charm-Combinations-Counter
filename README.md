# About

Quick-and-dirty program that enumerates (counts and lists) all possible charm combinations in Hollow Knight without being "overcharmed" or simply unable to equip more. According to this solution, there are 4,460,494 combinations of charms possible (including no charms) without exceeding the number of charm notches available (11) and incurring a penalty ("overcharmed").
This solution is suboptimal, but is just a lark and only only takes a minute or so to complete. The resulting text file, combos.txt, is about 800mb.
I may modify this in the future to accommodate "overcharmed" combinations (combinations exceeding 11 notches). I invite others to try to calculate those combinations before I do.

## Rules

 - There are 45 charms in the game and up to 11 notches to hold them. Different charms have different notch costs (or "weights"). For the purposes of this project, it is more useful to consider these three pairs as single charms, bringing the total down to 42.
     - The following 3 pairs of charms are counted as distinct, but they cannot coexist because they are upgrades:
	     - **Fragile Heart** &rarr; **Unbreakable Heart**
	     - **Fragile Greed** &rarr; **Unbreakable Greed**
    	 - **Fragile Strength** &rarr; **Unbreakable Strength**
- The following two pairs of charms cannot coexist because they require different choices during a playthrough. Grimmchild has multiple upgrade stages, but they are not considered unique by any wikis:
	- **Grimmchild I-IV**, **Carefree Melody**
- **Kingsoul** and **Voidheart** are also an upgrade pair that cannot coexist.
