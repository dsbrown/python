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
import boto.rds
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

# sql_action_statement - build SQL statement to put data into table
#   table is the SQL table to be effected
#   d data is a dictionary hash, walk through it and build SQL statement
#   action is 'INSERT' or 'REPLACE' depending on the desired side effect
#   INSERT is for new entries and will error if the entry exists
#   REPLACE will UPDATE an existing entry by replacing all matching fields
#sql_action_statement("SiteTbl","REPLACE",config.SiteTbl_desc,row)
def create_sql_statement(table,action,d,pk):

    sql_preamble = ""
    sql_postscript = ""
    sql_keys =" ( "
    sql_data = " Values (" 
    for key in d.keys():
        sql_keys+=key
        sql_data+="'%s'" % d[key]
        sql_keys+=", "
        sql_data+=", "
    sql_keys=sql_keys[:-2] # removes the final ", " 
    sql_data=sql_data[:-2]
    sql_data+=") "  
    sql_keys+=") "

    if action in ('INSERT',):
        sql_preamble = "INSERT INTO "+table
    if action in ('REPLACE',):
        sql_preamble = "REPLACE INTO "+table
    if action in ('DUPLICATE',):
        sql_preamble = "INSERT INTO "+table
        sql_postscript = " ON DUPLICATE KEY UPDATE "
        for key in d.keys():
            sql_postscript+=" %s='%s', " % (key,d[key])
        sql_postscript=sql_postscript[:-2]

    return sql_preamble+sql_keys+sql_data+sql_postscript

# build_query - builds a SQL search query based on the search_fiels passed
#   to it and getting values from the dictionry record
def build_query(record, search_fields): #Builds a SQL search query
    c=0
    query=""
    for i in search_fields:
        print "building query: %s"%str(record[i])
        if record.get(i):   #.get - doesn't error if if doesn't exist
            print "record has: %s"%str(record[i])
            if c:
                query+=" AND "
            c+=1
            query+=i+" = '"+str(record[i])+"'"
    return query

# write_record - Execute s the SQL statement typically an INSERT or REPLACE 
#   returns >=0 if success
#   returns -1 if failure 

def write_record(s, *args):
    try:
        logger.debug("SQL Statement: %s", s)
        affected_count = cursor.execute(s,args)
        mydb.commit()
        logger.info ("Wrote %d records ",affected_count)
        return cursor.lastrowid
    except MySQLdb.IntegrityError:
        logger.error( "failed to insert values, IntegrityError")
        return -1


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

######################
#   Connect to RDS 
######################
conn = boto.rds.connect_to_region("us-west-2")
instances = conn.get_all_dbinstances()
logger.debug( "Instances: " + str(instances))
instance = conn.get_all_dbinstances(config.db_instance)
db = instance[0]
endpoint,port = db.endpoint
logger.debug(  "endpoint [" + str(endpoint) + " " + str(port) + "]")
logger.debug(  "Connecting to MySQL using MySQLdb: "+ "host="+endpoint+","+"user="+config.db_user+","+"passwd="+config.db_password+","+"db="+config.db_name+","+"port="+str(port) )
mydb=MySQLdb.connect(host=endpoint,user=config.db_user,passwd=config.db_password,db=config.db_name,port=port)
cursor = mydb.cursor()
result = cursor.execute("SET NAMES 'utf8'") # forces connection to UTF-8


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
                    number = element.split("_")[1]
                except ValueError:
                    print "Found %s but expected Question_" % element

                #logger.debug("%s: %s", number, row[element])
                questions[number] = row[element]

        print "QuestionnaireGUID: %s DocEngVersion: %s" % (common['QuestionnaireGUID'], common['DocEngVersion'])

        # Query the database and try to find the QuestionNo and QuestionnaireGUID in the QuestionTbl that matches 
        query = "SELECT idQuestionTbl, QuestionNo, QuestionText FROM QuestionTbl WHERE "
        search_field =('QuestionnaireGUID', 'DocEngVersion')
        query += "( "+build_query(common,search_field)+" )"
        print query
        cursor.execute(query)
        #print "SQL Query: %s" % query
        row_results = cursor.fetchone()
        if row_results:  #We found a matching entry in the question database
            print "found previous entry"
            for row in row_results:
                if row:  #We found a matching question, this effects the SQL statement
                    (idQuestionTbl, QuestionNo, QuestionText) = row
                    question_pk[QuestionNo] = idQuestionTbl

        # Now write to the database
        for q_no in questions.keys():
            # alrighty, here is the problem the csv file has some strange encodings that no amount of normal wacking can fix
            # this little incantation does fix it, the key is unidecode, but the conversions are also necessary to avoid an error
            qtext = unidecode(questions[q_no].decode("cp1250"))
            qstext=qtext.encode("latin-1","ignore")
            escaped = mydb.escape_string(qstext) #this seems odd, but it does work use the connector not an internal call because well known error

            if question_pk.get(q_no):       # If the question was previously in database we need to overwrite it .get doesn't throw a key error
                print "Found it in the database"
                # d['idQuestionTbl'] = question_pk[q_no]
                # s = "INSERT INTO QuestionTbl ( idQuestionTbl, DocEngVersion, QuestionnaireGUID, QuestionNo, QuestionText)  Values (%d,%f,%s,%d,%s)"
                # record_id = write_record(s,d['idQuestionTbl'],d['DocEngVersion'],d['QuestionnaireGUID'],d['QuestionNo'],d['QuestionText']) 
                # if record_id < 0 :
                #     raise ValueError("Fatal: cant add/update question %s in databse using pk %s",questions[element], question_pk[element])
                #     sys.exit(10)
            else:                           # Question doesn't exisit in the database add it 
                s = "INSERT INTO QuestionTbl (QuestionnaireGUID, DocEngVersion, QuestionNo, QuestionText)  Values (%s,%s,%s,%s)"
                try:
                    logger.debug("SQL Statement: %s [%s,%s,%s,%s]", s,common['QuestionnaireGUID'], common['DocEngVersion'], q_no, escaped)
                    record_id = cursor.execute(s, ( common['QuestionnaireGUID'], common['DocEngVersion'], q_no, escaped)) 

                except MySQLdb.IntegrityError:
                    logger.error( "failed to insert values, IntegrityError")
                    sys.exit(10)

                mydb.commit()
                logger.info ("Wrote %d records ",record_id)


    filesProcessed.append(mfile)
logger.info("Files procesed: " + str(filesProcessed))

cursor.close()
mydb.close()
conn.close()
