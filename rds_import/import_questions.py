#!/usr/local/bin/python
# -*- coding: utf-8 -*-

###################################################################################
#
#                               Import Questions
#                               To RDS Database 
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
# v1.0  DSB      31 Mar 2015     Create import_questions
#
####################################################################################

import argparse
import sys
import csv
import config  # Global Settings
from dsb_rds import *
#import boto.rds
import MySQLdb
import time
from unidecode import unidecode # $ pip install unidecode
import logging, logging.config
from datetime import date, datetime, timedelta
logging.config.dictConfig(config.LOGGING)


parser = argparse.ArgumentParser(
    description='Read a question file and put those records in a mysql database on RDS'
    )

####################################################################################
#
#                               Create Arguments
#
####################################################################################

# Count of verbose flags such as: arg_parse.py -v, arg_parse.py -vv, arg_parse.py -vvv, etc
parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity, >= 3=Debug")

# Files to open, one by one as in csvparse.py -f foo.txt bar.txt fu.txt 
parser.add_argument("-f", "--files", nargs="+", dest="mfiles", help="file names to open separated by spaces")

# You may optionally change the delimeter and quote character
parser.add_argument('-d', '-delimiter', default=",", help="Optionally specify the field separation delimiter used, the default is ','")
parser.add_argument('-q', '-quote_delimiter', default='"', help="Optionally specify the quote delimiter that is being used, the default is \"")

parser.add_argument('--overwrite_question', action='store_true', default=False, help="If it encounters a duplicate question entry it will overwrite it with the data in the csv file. This is dangerious use with care.")

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
####################################################################################
#
#                                Functions
#
####################################################################################

####################################################################################
#
#                                   Main
#
####################################################################################
# Setup Logging 
args = parser.parse_args()
logger = logging.getLogger(__name__)

if args.verbose == 1:
    logging.basicConfig(level=logging.INFO)
elif args.verbose > 1:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logger.debug("args: %s", args)

#   Connect to RDS 

mydb = DsbRds()
mydb.connect()
mydb.create_cursor()

# Slurp up the csv files 

# into an array of dicts
# Add a Site UUID if one doesn't exist already
#
# Slurp up the csv files into a dictionary one at a time
# then look to see if the site already is in the database
# if it is, get the SiteUUID and PK SiteId_tbl, if not assign new ones
# Vaidate the data
filesProcessed = []
questions = {}    # put all question text in a dictionary one for each record keyed on question number
question_pk = {}
common = {}
record_count = 0
csv_count = 0

if args.mfiles:
    for mfile in args.mfiles:
        logger.debug("filename: %s", mfile)
        o = open(mfile,'rU')    #It will throw an error if not opened up in U mode
        reader = csv.DictReader(o)
        for row in reader:
            common['QuestionnaireGUID'] = row['QuestionnaireGUID']
            del row['QuestionnaireGUID']
            common['DocEngVersion'] = row['DocEngVersion']
            del row['DocEngVersion']
            for element in row.keys():
                try:
                    number = int(element.split("_")[1])
                except ValueError:
                    logger.warning("Found %s but expected Question_", element)
                questions[number] = row[element]
                csv_count += 1

        logger.debug("QuestionnaireGUID: %s DocEngVersion: %s", common['QuestionnaireGUID'], common['DocEngVersion'])
        logger.info("File: %s, found %s rows" % ( mfile,csv_count))
        # Query the database and try to find the QuestionNo and QuestionnaireGUID in the QuestionTbl that matches 
        # New found knowledge, the statment: 
        #           SELECT * FROM QuestionTbl WHERE  DocEngVersion = '2.32' 
        # Doesn't work, but statements like:
        #           SELECT * FROM QuestionTbl WHERE  DocEngVersion > '2.3'
        # Does, go figure, well actually I did; but I did't get it to work so I dropped from the search
        # since it is 100% useless to add it to the search 

        mydb.select( "QuestionTbl", 'idQuestionTbl', 'QuestionNo', QuestionnaireGUID=common['QuestionnaireGUID'] )

        row_results = mydb.get_cursor().fetchall()
        for (idQuestionTbl, QuestionNo) in row_results:
            question_pk[QuestionNo] = idQuestionTbl
  
        # Now write to the database
        for q_no in questions.keys():
            # alrighty, here is a problem, the csv file has some strange encodings that no amount of normal wacking can fix
            # this little incantation does fix it, the key is unidecode, but the conversions are also necessary to avoid an error
            qtext = unidecode(questions[q_no].decode("cp1250"))
            qstext=qtext.encode("latin-1","ignore")
            escaped = mydb.escape_string(qstext) #this seems odd, but it does work use the connector not an internal call because well known error

            logger.debug( "Question Number: %s with primary key: %s",q_no,question_pk.get(q_no) )
            if question_pk.get(q_no):       # If the question was previously in database we need to overwrite it .get doesn't throw a key error
                
                # "DELETE FROM QuestionTbl WHERE idQuestionTbl=%s" 
                logger.debug("entry with key  %s exists, deleting and adding", question_pk.get(q_no))
                delete_id = mydb.delete('QuestionTbl',idQuestionTbl=question_pk.get(q_no))
                record_id = mydb.write( "QuestionTbl", idQuestionTbl = question_pk.get(q_no), QuestionNo = q_no, QuestionText=escaped, **common )
            else:                           
                # Question doesn't exisit in the database add it 
                record_id = mydb.write( "QuestionTbl", QuestionNo = q_no, QuestionText=escaped, **common )

            mydb.commit()
            record_count+=record_id

    filesProcessed.append(mfile)
logger.info ("Wrote %d records ",record_count)
logger.info("Files procesed: " + str(filesProcessed))

mydb.close()

