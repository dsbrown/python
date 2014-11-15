#!/usr/bin/env python 
# -*- coding: utf-8 -*-

###################################################################################
#
# 							Basic Shell Program
#
# Description:
# This is my basic command line based program skeleton for creating other programs
#
# Author: David S. Brown
# Last Major Change: 14 November 2014
#
####################################################################################

import argparse
import sys
parser = argparse.ArgumentParser(description='A skeletal framework for writing command line based programs',
	epilog="And that's how you'd foo a bar",
	prefix_chars='-+',
	)

####################################################################################
#
# 							Debugging & Verbosity Flags
#
####################################################################################

# Count of verbose flags such as: arg_parse.py -v, arg_parse.py -vv, arg_parse.py -vvv, etc
parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")
# a numeric debug level as in arg_parse.py -D 3
parser.add_argument("-D", "--debug", type=int, default=0, help="Set integer debug level from 0-9 as: -D 3")
# a logical flag true or false as in arg_parse.py -q
parser.add_argument("-q", "--quiet", action="store_false", dest="verbose", default=True, help="Please be quiet, no output to stdout")



####################################################################################
#
# 									Filename Flags
#
####################################################################################
# MULTIPLE FILENAME METHOD 1 - use this to call files with -f example: arg_parse.py  -f foo.txt bar.txt fu.txt
#parser.add_argument("-f", "--files", nargs="+", dest="mfiles", help="file names to processed separated by spaces")

# MULTIPLE FILENAME METHOD 2 - use this to call files on the end of the command line example: arg_parse.py foo.txt bar.txt fu.txt
#parser.add_argument(nargs="+", dest="mfiles", help="file names to processed separated by spaces")

# MULTIPLE FILENAME METHOD 3 - use this to call files on the end of the command line example: arg_parse.py  -f foo.txt -f bar.txt -f fu.txt 
#parser.add_argument('-f', '--file', dest="mfiles", action='append', help="file names to processed in this format: -f file1 -f file2 -f file3")

# SINGLE FILENAME METHOD 1 - use this to call a file on the end of the command line example: ./arg_parse.py -vv foo.txt 
#parser.add_argument('inputfile', help="input file name to work on")

# SINGLE FILENAME METHOD 2 - use this to call a file on the end of the command line example: ./arg_parse.py -vv -f foo.txt 
#parser.add_argument('inputfile', help="input file name to work on")

# MULTIPLE FILENAME METHOD 4 - Allow Optional Input and output files using positional arguments
parser.add_argument('infile',  nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)


####################################################################################
#
# 									Other Flags
#
####################################################################################
#parser.add_argument("square", type=int, help="display a square of a given number")

#Here is a tri-mode flag - my terminology , see parser call above
#	./arg_parse.py  
#	Last =-1
#	./arg_parse.py -L 
#	Last =False
#	./arg_parse.py +L 
#	Last =True
parser.add_argument('-L', '-Last', action="store_false", default=-1, dest="Last", help="Do not assert Last")
parser.add_argument('+L', '+Last', action="store_true",  dest="Last", help="Assert Last")

# Some practical flags
parser.add_argument('-d', '-delimiter', default=",", help="Optionally specify the field separation delimiter used, the default is ','")
parser.add_argument('-i', '-interactive', action="store_true", default=False, 
	help="This will output helpful information about the file its processing and ask if you want to continue, the default is non-interactive",
	)

####################################################################################
#
# 									Demonstration Code
#
####################################################################################

args = parser.parse_args()


# Demonstration of numeric debug and verbose level also integer value
#
# print("Debug level: {}".format(args.debug))

# answer = args.square**2
# if args.debug >= 2:
# 	print("args: ", args)
# elif args.debug >= 1:
# 	print("n={}".format(args.square, args.square))
# else:
# 	True

# if args.verbose >= 2:
#    print("{}^2 == {}".format(args.square, answer))
# elif args.verbose >= 1:
#    print(answer)
# else:
#    print("the square of {} equals {}".format(args.square, answer))


# Demonstration Mutli file name method 1,2,3
#print(args.mfiles)

#Single file name demonstration method 1 & 2
#print(args.inputfile)
#for mfile in args.mfiles
#	print("filename:{}".format(mfile))

# Demonstration of stdin/stdout - Multi file name method 4
# call as ./arg_parse.py foo.txt bar.txt
print(args.infile, args.outfile)
print("Last ={}".format(args.Last))

