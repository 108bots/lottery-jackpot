# Lottery-Jackpot

Frustrated that your random picks or handcrafted picks are not hitting the MEGAMILLIONS or POWERBALL jackpot? 

Fret no more. Use this _Intelligent<sup>1</sup> program_ to generate your jackpot winning numbers. _$Gauranteed<sup>2</sup>$_

On a serious note, this code does the following:

- Reads a feed from https://data.ny.gov/ on historical drawing data
- Shows some unintersting stats to show that winning numbers are fairly uniformly distributed (for the most part) 
- Generates a weighted random sequence of numbers to try your luck

## Usage

    > python win_lotto.py --help
    usage: win_lotto.py [-h] --lotto LOTTO [--draw_aware] [--stats] [--jackpot] [--greedy]

    $$ Generate winning numbers for Megamillions & Powerball based on previous draws $$

    optional arguments:
      -h, --help     show this help message and exit
      --lotto LOTTO  mega OR power
      --draw_aware   If specified, white ball selection based on occurence in a draw position.
      --stats        If specified, will dump stats on all the numbers to CONSOLE and CSV. Required if --jackpot is not specified.
      --jackpot      If specified, will generate a JACKPOT worthy sequence of numbers. Required if --stats is not specified.
      --greedy       If specified, will only use above MEDIAN occuring numbers in JACKPOT sequence generation. Applicable only with -- 
                     jackpot argument.

## Examples

See sample csv and txt stat files for details

    > python win_lotto.py --lotto mega --jackpot

    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
     Your JACKPOT numbers for MEGAMILLIONS
     WHITE BALLS: [5, 28, 62, 65, 70]
     MEGABALL: 5
    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    > python win_lotto.py --lotto power --stats
    ########## RED BALL STATS #################
    Number of Draws: 737
        Lucky
        ^
        |
            Ball [24] was picked 5.02% of the time (37 instances)
            Ball [15] was picked 4.61% of the time (34 instances)
            Ball [7] was picked 4.34% of the time (32 instances)
            Ball [25] was picked 4.34% of the time (32 instances)
            Ball [13] was picked 4.21% of the time (31 instances)
            Ball [17] was picked 4.21% of the time (31 instances)
            Ball [19] was picked 4.21% of the time (31 instances)
            Ball [6] was picked 4.07% of the time (30 instances)
            Ball [8] was picked 4.07% of the time (30 instances)
            Ball [12] was picked 4.07% of the time (30 instances)
            Ball [9] was picked 3.93% of the time (29 instances)
            Ball [11] was picked 3.93% of the time (29 instances)
            Ball [20] was picked 3.93% of the time (29 instances)
            Ball [5] was picked 3.8% of the time (28 instances)
        |
        Neutral
        |
            Ball [10] was picked 3.8% of the time (28 instances)
            Ball [16] was picked 3.8% of the time (28 instances)
            Ball [22] was picked 3.8% of the time (28 instances)
            Ball [18] was picked 3.66% of the time (27 instances)
            Ball [1] was picked 3.53% of the time (26 instances)
            Ball [3] was picked 3.39% of the time (25 instances)
            Ball [23] was picked 3.39% of the time (25 instances)
            Ball [26] was picked 3.39% of the time (25 instances)
            Ball [2] was picked 3.26% of the time (24 instances)
            Ball [21] was picked 3.26% of the time (24 instances)
            Ball [4] was picked 3.12% of the time (23 instances)
            Ball [14] was picked 2.85% of the time (21 instances)
        |
        v
        Unlucky

    ########## WHITE BALL STATS ###############

    ****** Draw 1 Stats **********
        Number of Draws: 910
        Lucky
        ^
        |
             Ball [1] was picked 7.91% of the time (72 instances)
             Ball [3] was picked 7.03% of the time (64 instances)
             Ball [2] was picked 6.7% of the time (61 instances)
             Ball [5] was picked 6.59% of the time (60 instances)
             Ball [4] was picked 6.15% of the time (56 instances)
             Ball [9] was picked 5.16% of the time (47 instances)
    etc...



_<sup>1 Not really. No rocket science to beat your lottery odds here.</sup>_

_<sup>2 You knew that was a joke.</sup>_
