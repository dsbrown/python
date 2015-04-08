#!/usr/local/bin/python
# -*- coding: utf-8 -*-

###################################################################################
#
#                            Import Question Detail
#                               To RDS Database 
#
#
# Description:
#
# Given a CSV file with the first (column header) row being keys and the
# following rows being the values that correspond to the keys and
# question numbers (first column) column labeled 'Question#'. Create
# corresponding records in  a mysql database on RDS
#
#
# Author: David S. Brown
# v1.0  DSB      7 Apr 2015     Create import_Question Detail
#
####################################################################################

import argparse
import sys
import csv
import config  # Global Settings
from dsb_rds import *
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

parser.add_argument('--overwrite', action='store_true', default=False, help="If it encounters a duplicate question entry it will overwrite it with the data in the csv file, use with care.")

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

filesProcessed = []
record_count = 0

if args.mfiles:
    for mfile in args.mfiles:
        logger.debug("filename: %s", mfile)
        o = open(mfile,'rU')    #It will throw an error if not opened up in U mode
        reader = csv.DictReader(o)
        for row in reader:
            # here is the data we will need:
            # Question Number -> row['Question#']
            # QuestionnaireGUID ->  row['QuestionnaireGUID']
            # AssessmentGUID ->  row['AssessmentGUID']

            # Map CSV row to Database row, to avoid a # in a column name
            #   change Question# to QuestionNo
            row['QuestionNo'] = row['Question#'] 
            del row['Question#']

            # Look for an existing record in the QuestionDetailTbl
            #     Use data from these rows/columns: QuestionnaireGUID, AssessmentGUID, QuestionNo
            # If record in the QuestionDetailTbl exists, delete it
            mydb.select( "QuestionDetailTbl", 'idQuestionDetailTbl', QuestionNo=row['QuestionNo'], QuestionnaireGUID=row['QuestionnaireGUID'], AssessmentGUID=row['AssessmentGUID'],  )
            row_results = mydb.get_cursor().fetchall()
            for (pk,) in row_results:
                if not args.overwrite_site:
                    print "Found question has been previously defined not adding it, use --overwrite to override"
                    sys.exit(1)
                logger.debug("Deleting QuestionDetailTbl pk: %s ", pk)
                delete_id = mydb.delete('QuestionDetailTbl',idQuestionDetailTbl=pk)

            # Look for reference in AssessmentResultsTbl
            #     Use data from these rows/columns: QuestionnaireGUID, AssessmentGUID
            #     If found get PK 
            #     If not found throw error?
            mydb.select( "AssessmentResultsTbl", 'idAssessmentTable', AssessmentGUID=row['AssessmentGUID'],)
            row_results = mydb.get_cursor().fetchall()
            if len(row_results) > 1:
                logger.warning("Found more than one AssessmentResults for File %s, AssessmentGUID=%s", mfile, row['AssessmentGUID'])
            elif len(row_results) == 0:
                logger.warning("No Assessment summary found for File %s, AssessmentGUID=%s, please import the AssessmentResults summary before the detail", mfile, row['AssessmentGUID'])
                sys.exit(2)
            AssessmentResultsIdxPK, = row_results[0]
            
            # Look for reference in QuestionTbl
            #     Use data from these rows/columns: QuestionnaireGUID, QuestionNo
            #     If found get PK
            #     If not found throw error
            mydb.select( "QuestionTbl", 'idQuestionTbl', QuestionnaireGUID=row['QuestionnaireGUID'], QuestionNo=row['QuestionNo'])
            row_results = mydb.get_cursor().fetchall()
            if len(row_results) > 1:
                logger.warning("Found more than one QuestionTbl for File %s, QuestionnaireGUID=%s", mfile, row['QuestionnaireGUID'])
            elif len(row_results) == 0:
                logger.warning("No Questions  found for File %s, QuestionnaireGUID=%s, please import the QuestionTbl before the Assessment details", mfile, row['QuestionnaireGUID'])
                sys.exit(2)
            QIdPK, = row_results[0]

            # We are ready to write the record
            #     We got FK: QId, AssessmentResultsIdx, 
            #     Foreign key mappings:
            #         QId -> QuestionTbl (PK) = idQuestionTbl
            #         AssessementResultsIdx -> AssessmentResultsTbl (PK) = idAssessmentTable      

            #     Now write the record
            #dsb - problem here with QId AssessmentResultsIdx
            row['QId']=QIdPK
            row['AssessmentResultsIdx']=AssessmentResultsIdxPK
            record_id = mydb.write( "QuestionDetailTbl", **row  )
            logger.info("Wrote record")
        
            mydb.commit()
            record_count+=record_id

    filesProcessed.append(mfile)
logger.info ("Wrote %d records ",record_count)
logger.info("Files procesed: " + str(filesProcessed))

mydb.close()

