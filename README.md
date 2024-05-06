# About

This is a rewrite of SJT1988's project which uses dynamic programming to speed things up (about 7x faster on my machine), and optionally allows overcharmed combinations too.

## How Many Charm Combinations Are There In Hollow Knight?

Without exceeding 11 charm notches and being "overcharmed", there are **4,460,494** combinations of charms possible in *Hollow Knight*, and with overcharmed combinations being permitted, it is instead **23,776,564**.  
The resulting text file, combos.txt, is about 471MB and 2.7GB with and without overcharmed combinations permitted. (This is reduced to 79MB and 465MB if the alternative encoding is used)  
You can find pre-generated versions of these files in this repo compressed with xz. 

## Rules

 - There are 45 charms in the game and up to 11 notches to hold them. Different charms have different notch costs (or "weights"). For the purposes of this project, it is simpler to consider these three pairs as single charms, bringing the total number of charms down to 42.
     - The following 3 pairs of charms are counted as distinct, but they cannot coexist because they are upgrades:
	     - **Fragile Heart** &rarr; **Unbreakable Heart**
	     - **Fragile Greed** &rarr; **Unbreakable Greed**
    	 - **Fragile Strength** &rarr; **Unbreakable Strength**
- The following two pairs of charms cannot coexist because they require different choices during a playthrough. Grimmchild has multiple upgrade stages, but they are not considered unique by any wikis:
	- **Grimmchild I-IV**, **Carefree Melody**
- **Kingsoul** and **Voidheart** are also an upgrade pair that cannot coexist.

# Usage

Clone the repository and run `python HK_charms_combo_counter.py`.  
By default, this will count all combinations, including overcharmed ones, and write all of them to `combos.txt`. For more options, pass it the `-h` flag.  
I highly recommend installing the `tqdm` Python module for progress bars. The program will still run fine without it, just without progress bars.