#!/usr/bin/env python 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int, help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2

# bugfix: replace == with >=
if args.verbosity >= 2:
    print("the square of {0:s} equals {1:s}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{0:s}^2 == {1:s}".format(args.square, answer))
else:
    print(answer)
