#!/usr/bin/env python 
# -*- coding: utf-8 -*-

###################################################################################
#
# 						   CSV to RDS SQL Program
#
# Description:
# Given a CSV file with the first (header) row being keys and the following rows
# being the values that correspond to the keys. Create corresponding records in 
# a mysql database on RDS and insert the data into a prior defined database.
# The key value pairs are inserted into dicts and we create an array of dicts
# for corresponding to each row of the csv spread sheet.
# 
#
# Author: David S. Brown
# v1.0	DSB		Create csv2sql
#
####################################################################################

import argparse
import sys
import csv

parser = argparse.ArgumentParser(
	description='Create records in a mysql database on RDS and insert the data from'\
				'a predefined and constructed database'
	)

####################################################################################
#
# 						 		Create Arguments
#
####################################################################################

# Count of verbose flags such as: arg_parse.py -v, arg_parse.py -vv, arg_parse.py -vvv, etc
parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity, 3=Debug")

# Files to open, one by one as in csvparse.py -f foo.txt bar.txt fu.txt 
parser.add_argument("-f", "--files", nargs="+", dest="mfiles", help="file names to open separated by spaces")

# You may optionally change the delimeter and quote character
parser.add_argument('-d', '-delimiter', default=",", help="Optionally specify the field separation delimiter used, the default is ','")
parser.add_argument('-q', '-quote_delimiter', default='"', help="Optionally specify the quote delimiter that is being used, the default is \"")

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
####################################################################################
#
# 								 Functions
#
####################################################################################

def sql_insert_statement(table,d):
	sql_keys ="INSERT INTO "+table+" ("
	sql_data = "Values ("
	for key in d.keys():
		sql_keys+=key   
		sql_data+=d[key]
		sql_keys+=", "
		sql_data+=", "
	sql_keys=sql_keys[:-2] # removes the final ", " 
	sql_data=sql_data[:-2]
	sql_data+=") "	
	sql_keys+=") "
	return sql_keys+sql_data
	
		
####################################################################################
#
# 									Main
#
####################################################################################

# Slurp up the csv files into an array of dicts
args = parser.parse_args()
if args.verbose >=2 : print("args: ", args)

#
# Open files and if interactive examine the file to see if the header is present
#
filesProcessed = []
data = []
if args.mfiles:
	for mfile in args.mfiles:
	
		if args.verbose >=1 : print("filename:{}".format(mfile))

		o = open(mfile,'rU')
		reader = csv.DictReader(o)
		for row in reader:
			data.append(row)
			if args.verbose >=3 : print(row)
	filesProcessed.append(mfile)

if args.verbose >= 1:
	print("Files procesed: " + str(filesProcessed))

for record in data:
	s = sql_insert_statement("foo",record)
	print s
