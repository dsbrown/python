#!/usr/local/bin/python
# -*- coding: utf-8 -*-

###################################################################################
#
#                          CSV to RDS SQL Program
#
# Description:
# Given a CSV file with the first (header) row being keys and the following rows
# being the values that correspond to the keys. Create corresponding records in 
# a mysql database on RDS and insert the data into a prior defined database.
# The key value pairs are inserted into dicts and we create an array of dicts
# for corresponding to each row of the csv spread sheet.
#
# Known Problems:
# This program, when its working will be fine for a first insert, but it doesn't
# check to see if a site or assesment is pre-existing and update it, it just 
# happily duplicates the records.
# 
#
# Author: David S. Brown
# v1.0  DSB     Create csv2sql
#
####################################################################################

import argparse
import sys
import csv
import config  # Global Settings
import uuid
import boto.rds
import MySQLdb
import time
import logging, logging.config
from datetime import date, datetime, timedelta
logging.config.dictConfig(config.LOGGING)






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
parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity, >= 3=Debug")

# Files to open, one by one as in csvparse.py -f foo.txt bar.txt fu.txt 
parser.add_argument("-f", "--files", nargs="+", dest="mfiles", help="file names to open separated by spaces")

# You may optionally change the delimeter and quote character
parser.add_argument('-d', '-delimiter', default=",", help="Optionally specify the field separation delimiter used, the default is ','")
parser.add_argument('-q', '-quote_delimiter', default='"', help="Optionally specify the quote delimiter that is being used, the default is \"")

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
####################################################################################
#
#                                Functions
#
####################################################################################

# Looks at a string and tries to interpret if it is an INT, FLOAT or STR
def is_it_a_number(text):
    try:
        int(text)
        return 'INT'
    except ValueError:
        pass

    try:
        float(text)
        return 'FLOAT'
    except ValueError:
        pass
    return 'STR'

# data is an array of dicts, need to walk through the arrays printing each dict
def sql_insert_statement(table,d):
    sql_keys ="INSERT INTO "+table+" ("
    sql_data = "Values ("
    for key in d.keys():
        sql_keys+=key   
        sql_data+="'"+str(d[key])+"'"
        sql_keys+=", "
        sql_data+=", "
    sql_keys=sql_keys[:-2] # removes the final ", " 
    sql_data=sql_data[:-2]
    sql_data+=") "  
    sql_keys+=") "
    return sql_keys+sql_data

#This validates the fields and the data in d and hands back another array 
#  of type d with only field names that match the database field names
#  and data that is actually valid for the database field type
#  it silently throws away fields that don't match and THIS IS IMPORTAINT
#  it adds the SiteUUID to all records it returns, this is so we can later
#  reconnect the entries if we need to, otherwise we lose the connection
#  between the data.
#  field definitions are in config
def valid_dicts(d,field_desc): #  (array of dicts, list of valid fields)
    dreturn = []
    valid = field_desc.keys()

    for record in d:  #Again with the list of dictonaries ...
        e = {}
        e['SiteUUID'] = record['SiteUUID'] # Everybody gets SiteUUID its how we tie things together
        for key in record.keys():
            if key in valid:
                #examine and validate data in each field
                if field_desc[key] ==  'INT':
                    if str(record[key]) in ('x','X','1'):
                        e[key]='1'
                    elif str(record[key]) in ('','0'):
                        e[key]='0'
                    elif is_it_a_number(record[key]) in ('INT','FLOAT'):
                        e[key]=str(record[key])
                    else:
                        e[key]='1'
                        logger.warning("Warning, INT: "+str(record[key])+" converted to 1")
                elif field_desc[key] in ('DOUBLE', 'FLOAT'):
                    if is_it_a_number(record[key]) in ('INT','FLOAT'):
                        e[key]=str(record[key])
                    else:
                        logger.warning( "Warning, FLOAT: "+str(record[key])+" wants to be a number, but cant be")
                #elif field_desc[key]in ('DATETIME'):   # date format typicaly: 5/6/2015
                #not implmented until we determine the case
                else:
                    e[key]=record[key]
        dreturn.append(e)
    return dreturn

####################################################################################
#
#                                   Main
#
####################################################################################
#
# Slurp up the csv files into an array of dicts
#
args = parser.parse_args()



logger = logging.getLogger(__name__)

if args.verbose == 1:
    logging.basicConfig(level=logging.INFO)
elif args.verbose > 1:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


logger.debug("args: %s", args)

filesProcessed = []
data = []
if args.mfiles:
    for mfile in args.mfiles:
    
        logger.debug("filename: %s", mfile)

        o = open(mfile,'rU')    #It will throw an error if not opened up in U mode
        reader = csv.DictReader(o)
        for row in reader:
            row['SiteUUID'] = uuid.uuid4()   # Add a SiteUUID for every dict in the array according to RFC 4122, uuid4 is more secure than uuid1
            data.append(row)
            #logger.debug("Row %s",row)
    filesProcessed.append(mfile)
    logger.info("Files procesed: " + str(filesProcessed))
#
# Validate fields per table, only include fields that are part 
# of this table, toss all others out

SiteTbl_dicts=valid_dicts(data,config.SiteTbl_desc)
#logger.debug("Site Dictionary: " + str(SiteTbl_dicts))
    
AssessmentResultsTbl_dicts=valid_dicts(data,config.AssessmentResultsTbl_desc)
#logger.debug("Assessment Dictionary: " + str(AssessmentResultsTbl_dicts))

# AuditResultsTbl Not implemented because no csv data at this time this will probably will be a seperate program

# Connect to RDS 
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

def build_query(record,search_fields):
    c=0
    query=""
    for i in search_fields:
        if record.get(i):
            if c:
                query+=" AND "
            c+=1
            query+=i+" = '"+record[i]+"'"
    return query

# Writes the record to the database
#   takes s the SQL statement to do the insert 
#   returns 1 if success and sets record_id to the record id written,
#   returns 0 if failure and sets record_id = -1 
def write_record(s,record_id):
    try:
        logger.debug("SQL Statement: %s", s)
        affected_count = cursor.execute(s)
        mydb.commit()
        logger.info ("Wrote record: "+str(affected_count))
        record_id = cursor.lastrowid
        return 1
    except MySQLdb.IntegrityError:
        logger.error( "failed to insert values")
        record_id = -1
        return 0

# turn list of dictionaries into SQL statement and write it for SiteTbl
#UNDER CONSTRUCTION!
# Ensure successful write and then get row number
#Future: should check and see if Site exists already before writing it!
# First Look for duplicate site records 
# if we find it, we will correct the SiteUUID
#



for record in SiteTbl_dicts:
    record_id=-1
    # First look into the database and try to determine if the site already exists
    query = "SELECT SiteId_tbl, SiteUUID FROM SiteTbl WHERE "
    search_fields1 =('VendorSiteLatitude', 'VendorSiteLongitude')
    search_fields2 =('VendorName','VendorSiteName','VendorSiteAddress','VendorSiteCity','VendorSiteState','VendorSiteCountry')
    # Look and see if the site already exists, if it does don't add it again
    # build query of site info
    query += "( "+build_query(record,search_fields1)+" ) OR ( "+build_query(record,search_fields2)+" )"
    previous_SiteUUID = record['SiteUUID']

    cursor.execute(query)
    row_results = cursor.fetchone() 
    if row_results:
        (SiteId_tbl_val, SiteUUID_val) = row_results
        if SiteUUID_val:
            # If Site previously exists, use its UUID in both tables
            logger.info("Found site has been previously defined not adding it ")
            #print " SiteId_tbl_val :"+str(SiteId_tbl_val)+" SiteUUID_val "+str(SiteUUID_val) 
            
            record['SiteUUID'] = SiteUUID_val
            record_id = SiteId_tbl_val

            # Loop through the other table(s) and update the SiteUUID and row number where appropriate
            for record2 in AssessmentResultsTbl_dicts:
                if str(record2['SiteUUID']) == str(previous_SiteUUID):
                    record2['SiteUUID'] = SiteUUID_val
                    record2['SiteId'] = SiteId_tbl_val
        else:
            raise Fatal_Data("Fatal: cursor returns value but its not SiteUUID, this is very confusing")
            sys.exit(10)
    else:
        logger.info( "Site doesnt exist in the site table ,adding it")
        # Site doesn't exists, so create it
        s = sql_insert_statement("SiteTbl",record)
        logger.debug ("SQL insert statement %s",s)
        if write_record(s,record_id) == 0:
            # Loop through the other table(s) and update the row number 
            for record2 in AssessmentResultsTbl_dicts:
                if str(record2['SiteUUID']) == str(previous_SiteUUID):
                    record2['SiteId'] = record_id
        else:
            raise Fatal_Data("Fatal: cant write Site Record")
            sys.exit(10)

    cursor.fetchall() # the docs say you need to fetch all rows before doing another query ->void

# Use row number above to write record below
# turn list of dictionaries into SQL statement and write it
# AssessmentResultsTbl
for record in AssessmentResultsTbl_dicts:
    #First check and see if the Assessment is already in the database
    query = "SELECT AssessmentGUID FROM AssessmentResultsTbl WHERE "
    search_fields = ('AssessmentGUID',)
    query += build_query(record,search_fields)
    logger.debug("Assessment Query: "+query)

    cursor.execute(query)
    row_results = cursor.fetchone() 
    if row_results:
        (AssessmentGUID) = row_results
        logger.info("Asessment exists, not updating")
    else:
        s = sql_insert_statement("AssessmentResultsTbl",record)
        if write_record(s,record_id) == 0:
            raise Fatal_Data("Fatal: cant write Assessment Record")
            sys.exit(11)
    cursor.fetchall()

cursor.close()
mydb.close()
conn.close()
