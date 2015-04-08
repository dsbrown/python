#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import config  # Global Settings
import boto.rds
import MySQLdb
import time
import argparse

parser = argparse.ArgumentParser(
    description='Create records in a mysql database on RDS and insert the data from'\
                'a predefined and constructed database'
    )

####################################################################################
#
#                               Create Arguments
#
####################################################################################

# Count of verbose flags such as: arg_parse.py -v, arg_parse.py -vv, arg_parse.py -vvv, etc
parser.add_argument('--site', action='store_true', default=False, help="Print Site Table.")
parser.add_argument('--assessment', action='store_true', default=False, help="Print Assessment Table")
parser.add_argument('--question', action='store_true', default=False, help="Print Question Table")
parser.add_argument('--detail', action='store_true', default=False, help="Print Question Detail Table")
parser.add_argument('--all', action='store_true', default=False, help="Print All Tables")

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

if  args.all:
    args.site = True 
    args.assessment = True
    args.question = True 
    args.detail = True 

# Connect to RDS 
conn = boto.rds.connect_to_region("us-west-2")
instances = conn.get_all_dbinstances()

instance = conn.get_all_dbinstances(config.db_instance)
db = instance[0]
endpoint,port = db.endpoint

print "Connecting to MySQL using MySQLdb: ", "host="+endpoint+","+"user="+config.db_user+","+"passwd="+config.db_password+","+"db="+config.db_name+","+"port="+str(port)
mydb=MySQLdb.connect(host=endpoint,user=config.db_user,passwd=config.db_password,db=config.db_name,port=port)
print "Connected to MySQL: "
cursor = mydb.cursor()
if  args.site:
    print "------------------------------------------------------------------"
    print "SiteTbl Table"
    print "------------------------------------------------------------------"

    query = "SELECT * FROM SiteTbl"
    cursor.execute(query)
    print "SiteTbl Table"
    row = cursor.fetchone()
    while row is not None:
        print (row)
        row = cursor.fetchone()

if  args.assessment:
    print "------------------------------------------------------------------"
    print "AssessmentResultsTbl Table"
    print "------------------------------------------------------------------"
    query = "SELECT * FROM AssessmentResultsTbl"
    cursor.execute(query)
    print "AssessmentResultsTbl Table"
    row = cursor.fetchone()
    while row is not None:
        print (row)
        row = cursor.fetchone()



if  args.question:
    print "------------------------------------------------------------------"
    print "QuestionTbl Table"
    print "------------------------------------------------------------------"
    print "Question Table"
    query = "SELECT * FROM QuestionTbl"
    cursor.execute(query)
    print "QuestionTbl Table"
    row = cursor.fetchone()
    while row is not None:
        #print "------------------------------------------------------------------"
        print (row)
        row = cursor.fetchone()

if  args.detail:
    print "------------------------------------------------------------------"
    print "QuestionDetailTbl Table"
    print "------------------------------------------------------------------"
    print "Question Detail Table"
    query = "SELECT * FROM QuestionDetailTbl"
    cursor.execute(query)
    print "QuestionDetailTbl Table"
    row = cursor.fetchone()
    while row is not None:
        #print "------------------------------------------------------------------"
        print (row)
        row = cursor.fetchone()

cursor.close()
mydb.close()
conn.close()
