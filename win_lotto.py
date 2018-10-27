from __future__ import division
import requests
import argparse
import sys
import random
import operator
import csv

"""
    win_lotto: Generate winning numbers and historical stats for MEGAMILLIONS & POWERBALL based on previous draws
"""

def weighted_random_ball(weights):
    remaining_dist = random.random() * sum(weights)
    for ball, weight in enumerate(weights):
        remaining_dist -= weight
        if remaining_dist < 0:
            return ball

parser = argparse.ArgumentParser(description='$$ Generate winning numbers for Megamillions & Powerball based on previous draws $$')
parser.add_argument('--lotto', required=True, help='mega OR power')
parser.add_argument('--draw_aware', required=False, action='store_true', help='If specified, white ball selection based on occurence in a draw position.')
parser.add_argument('--stats', required=False, action='store_true', help='If specified, will dump stats on all the numbers to CONSOLE and CSV. Required if --jackpot is not specified.')
parser.add_argument('--jackpot', required=False, action='store_true', help='If specified, will generate a JACKPOT worthy sequence of numbers. Required if --stats is not specified.')

args = parser.parse_args()

if not args.jackpot and not args.stats:
    parser.error('--stats or --jackpot args is required. See --help.')

lotto = args.lotto.lower()

if lotto == 'mega':
    lotto_api = 'https://data.ny.gov/resource/h6w8-42p9.json'
    red_min = 1
    red_max = 25
    white_min = 1
    white_max = 70
elif lotto == 'power':
    lotto_api = 'https://data.ny.gov/resource/8vkr-v8vh.json'
    red_min = 1
    red_max = 26
    white_min = 1
    white_max = 69
else:
    parser.error('Invalid <lotto> value. See --help.')

"""
    Query historical winning numbers
"""
headers = requests.utils.default_headers()
req = requests.get(lotto_api, headers=headers)
if req.status_code != 200:
    sys.exit("Lotto draw data unavailable")
lotto_data = req.json()

"""
    Initialize red ball count & weights with index as ball number and value as count of appearences with index 0 being a dummy
"""
red_balls = [0]*(red_max + 1)
red_weights = [0]*(red_max + 1)

"""
    Initialize white balls count & weights tuple of lists with list index as ball number and value as count of appearences with 
    index 0 being a dummy
    List 0 - 4 in the tuple hold white balls seen in each of the 5 draws
    List 5 holds white balls seen any of the 5 draws
"""
white_balls = (
    [0]*(white_max + 1),
    [0]*(white_max + 1),
    [0]*(white_max + 1),
    [0]*(white_max + 1),
    [0]*(white_max + 1),
    [0]*(white_max + 1)
)
white_weights = (
    [0]*(white_max + 1),
    [0]*(white_max + 1),
    [0]*(white_max + 1),
    [0]*(white_max + 1),
    [0]*(white_max + 1),
    [0]*(white_max + 1)
)

"""
    Count the number of occurences of each of the numbers
"""
for data in lotto_data:
    winning_list = data['winning_numbers'].split()
    win_list_size = len(winning_list)
    if lotto == 'mega':
        red_ball = int(data['mega_ball'])
    if lotto == 'power':
        red_ball = int(winning_list[win_list_size-1])
        win_list_size -= 1
    if red_ball >= red_min and red_ball <= red_max:
        red_balls[red_ball] += 1

    for item in range(win_list_size):
        ball = int(winning_list[item])
        if ball >= white_min and ball <= white_max:
            white_balls[item][ball] += 1
            white_balls[win_list_size][ball] += 1

"""
    Compute weight for each red number
"""
red_draws = sum(red_balls)
for itr in range(1, red_max+1):
    if red_balls[itr] > 0:
        red_weights[itr] = round ((red_balls[itr] / red_draws), 4)

"""
    Compute weight for each white number
"""
for i in range(len(white_balls)):
    white_draws = sum(white_balls[i])
    for itr in range(1, white_max+1):
        if white_balls[i][itr] > 0:
            white_weights[i][itr] = round ((white_balls[i][itr] / white_draws), 4)

"""
    Generate JACKPOT numbers
"""
if args.jackpot:
    """
       Draw the 5 lucky whites
    """
    lucky_whites = [0]*5
    if not args.draw_aware:
        for i in range(5):
            pick = weighted_random_ball(white_weights[5])
            while pick in lucky_whites:
                pick = weighted_random_ball(white_weights[5])
            lucky_whites[i] = pick
    else:
        for i in range(5):
            pick = weighted_random_ball(white_weights[i])
            while pick in lucky_whites:
                pick = weighted_random_ball(white_weights[i])
            lucky_whites[i] = pick

    """
        Draw the lucky red
    """
    lucky_red = weighted_random_ball(red_weights)

    """
        Print your jackpot numbers
    """
    banner = 'Unknown'
    if lotto == 'mega':
        banner = 'MEGAMILLIONS'
    if lotto == 'power':
        banner = 'POWERBALL'

    print "\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    print " Your JACKPOT numbers for %s" % banner
    print " WHITE BALLS: %s" % lucky_whites
    print " %sBALL: %s" % (lotto.upper(), lucky_red)
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"

"""
    Dump Stats
"""
if args.stats:
    print "\n########## RED BALL STATS #################"
    print "Number of Draws: %s" % red_draws
    red_balls_sorted = sorted([(i, j) for i, j in enumerate(red_balls)], reverse=True, key=operator.itemgetter(1))
    red_weights_sorted = sorted([(i, j) for i, j in enumerate(red_weights)], reverse=True, key=operator.itemgetter(1))
    red_file_name = lotto+'_red_ball.csv'
    with open(red_file_name, mode='w') as red_file:
        red_writer = csv.writer(red_file, delimiter=',')
        red_writer.writerow(['Ball','Times Drawn', 'Percentage Drawn'])
        print "    Lucky"
        print "    ^"
        print "    |"
        for i in range(len(red_balls_sorted)):
            if red_balls_sorted[i][0] == 0:
                continue
            if i == round(len(red_balls_sorted)/2):
                print "    |\n    Neutral\n    |" 
            print "        Ball [%s] was picked %s%s of the time (%s instances)" % (red_balls_sorted[i][0], red_weights_sorted[i][1]*100, '%', red_balls_sorted[i][1])
            red_writer.writerow([red_balls_sorted[i][0], red_balls_sorted[i][1], round(red_weights_sorted[i][1]*100, 2)])
        print "    |"
        print "    v"
        print "    Unlucky"
    
    print "\n########## WHITE BALL STATS ###############"
    for itr in range(len(white_balls)):
        white_file_name = lotto+'_white_balls_draw_'+str(itr+1)+'.csv'
        if itr == len(white_balls)-1:
            print "\n    ****** ALL Draw Stats **********"
            white_file_name = lotto+'_white_balls_draw_all.csv'
        else:
         print "\n    ****** Draw %s Stats **********" % (itr+1)
        print "        Number of Draws: %s" % sum(white_balls[itr])
        white_balls_sorted = sorted([(i, j) for i, j in enumerate(white_balls[itr])], reverse=True, key=operator.itemgetter(1))
        white_weights_sorted = sorted([(i, j) for i, j in enumerate(white_weights[itr])], reverse=True, key=operator.itemgetter(1))
        with open(white_file_name, mode='w') as white_file:
            white_writer = csv.writer(white_file, delimiter=',')
            white_writer.writerow(['Ball','Times Drawn', 'Percentage Drawn'])        
            print "        Lucky"
            print "        ^"
            print "        |"
            for i in range(len(white_balls_sorted)):
                if white_balls_sorted[i][0] == 0:
                    continue
                if i == round(len(white_balls_sorted)/2):
                    print "        |\n        Neutral\n        |"                
                print "             Ball [%s] was picked %s%s of the time (%s instances)" % (white_balls_sorted[i][0], white_weights_sorted[i][1]*100, '%', white_balls_sorted[i][1])
                white_writer.writerow([white_balls_sorted[i][0], white_balls_sorted[i][1], round(white_weights_sorted[i][1]*100, 2)])
            print "        |"
            print "        v"
            print "        Unlucky"

