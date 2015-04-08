#!/usr/local/bin/python
# -*- coding: utf-8 -*-

###################################################################################
#
#                  Import to Combined Site & Assessment CSV File
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
# v1.0  DSB      7 Mar 2015     Create csv2sql
# v1.1  DSB     18 Mar 2015     Modified to be simplier, doesn't use as 
#                                   complex data structure
# v1.2  DSB     25 Mar 2015     Modified to actualy work - Yea! Now meets 
#                                   all original requirements
# v1.2  DSB     31 Mar 2015     Still the same program but renamed 
# v1.3  DSB      7 Mar 2015     A big revision, brought in dsb_rds DsbRds module 
#                                   cut lots of lines 
####################################################################################

import argparse
import sys
import csv
import config  # Global Settings
import uuid
from dsb_rds import *
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

parser.add_argument('--overwrite_site', action='store_true', default=False, help="If it encounters a duplicate site entry it will overwrite it with the data in the csv file. This is dangerious use with care.")
parser.add_argument('--overwrite_assessment', action='store_true', default=False, help="If it encounters a duplicate assessment entry it will overwrite it with the data in the csv file. This is dangerious use with care.")

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

####################################################################################
#
#                                Functions
#
####################################################################################

#This accepts a date string of the form 5/6/2015 or 5/6/15
def TryDateParse(datestring):
    dateformats = ("%m/%d/%y","%m/%d/%Y")
    succes = False
    for aformat in dateformats:
        try:
            mydate = time.strptime(datestring,aformat)
            succes = True
            break
        except:
            pass
    if not succes:
        return False
    else:
        return mydate

# valid_dictionary - Given a dictionary d of {field_name : field_value,,,} and
# a dictionary field_desc of {field_name : field_type,,} return a third
# dictionary which contains only field_names in field_desc 
# Also, some of the flag fields of type INT may be set to on or off using 
# things like 1/0 Y/N etc. this needs to be standarized to 1 or 0 and
# the date needs to be put in a known format to import into the database

def valid_dictionary(d,field_desc): #  (d dictionary of data, dictionary of valid fields and types)
    valid = field_desc.keys()
    e = {}
    for key in d.keys():
        if key in valid:
            if d[key]:
                #examine and validate data in each field
                if field_desc[key] is 'INT':
                    if str(d[key]) in ('1','y','Y','x','X'):
                        e[key]=1
                    elif str(d[key]) in ('','0','n','N'):
                        e[key]=0
                    else:
                        e[key]=d[key]
                elif field_desc[key] in ('DATETIME') and d[key]:  # date format typicaly: 5/6/15
                    mydate = TryDateParse(d[key])
                    if not mydate:
                        print "Fatal: can't convert date [%s] to date" % d[key]
                        raise ValueError("Fatal: can't convert date %s to date" % d[key])
                        sys.exit(110)
                        #YYYY-MM-DD HH:MM:SS
                    e[key] = time.strftime("%Y-%m-%d %H:%M:%S",mydate)
                    #print "Formated Time %s" % (e[key])
                else:
                    e[key]=d[key]
            else:
                e[key]=None
    return e

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

if args.mfiles:
    for mfile in args.mfiles:
        logger.debug("filename: %s", mfile)
        o = open(mfile,'rU')    #It will throw an error if not opened up in U mode
        reader = csv.DictReader(o)
        for row in reader:
            ####################################
            # Process Site Informaton
            # Query the database and try to find a Site in the Site Table that matches this one
            # If found get the SiteUUID and PK, if required, overwrite the Site Data
            ####################################
            mydb.build_search( "SiteTbl", ["SiteId_tbl", "SiteUUID"], {'VendorSiteLatitude':row['VendorSiteLatitude'], 'VendorSiteLongitude':row['VendorSiteLongitude']})
            mydb.build_search_or(\
                {'VendorName':row['VendorName'],'VendorSiteName':row['VendorSiteName'],'VendorSiteAddress':row['VendorSiteAddress'],\
                'VendorSiteCity':row['VendorSiteCity'],'VendorSiteState':row['VendorSiteState'],'VendorSiteCountry':row['VendorSiteCountry'],}\
                )
            cursor = mydb.search_execute()            

            row_results = cursor.fetchone()
            if row_results:  #We found the site, interesting fact: the SiteUUID can never be replaced, must use existing one
                (SiteId_tbl_val, SiteUUID_val) = row_results

                 # If Site previously exists, replace its UUID  in the data structure
                if SiteUUID_val:       
                    if not args.overwrite_site:
                        print "Found site has been previously defined not adding it, use --overwrite_site to override "
                    #Set the SiteUUID to be the UUID we found in the database and get the Primary Key
                    logger.debug("SiteUUID was found, changing it to: %s",SiteUUID_val)
                    row['SiteUUID'] = SiteUUID_val
                else:
                    raise ValueError("Fatal: cursor (database) returns value but its not SiteUUID, this is very confusing")
                    sys.exit(10)

                # If Site previously exists, replace its PK row number in the data structure SiteId for Site, SiteId_tbl for Assessment
                if SiteId_tbl_val:   
                    row['SiteId_tbl'] = SiteId_tbl_val  # key  for SiteTbl
                    row['SiteId'] = SiteId_tbl_val      # key for AssessmentResultsTbl_
                    logger.debug("Row Number will be : %s",SiteId_tbl_val)
                else:
                    raise ValueError("Fatal: cursor (database) returns value but its not SiteId_tbl, this is very confusing")
                    sys.exit(10)

                # The site exists, but we need to overwrite the site info
                if args.overwrite_site: 
                    logger.info( "Overwriting site info")
                    e=valid_dictionary(row,config.SiteTbl_desc)
                    #print e
                    logger.debug("entry in the Site Table with  key  %s exists, and foreign key constraint %s using mysql UPDATE", row['SiteId_tbl'], row['SiteId'])
                    id = mydb.update('SiteTbl','SiteId_tbl',row['SiteId_tbl'],**e)
                    #record_id = mydb.write( 'SiteTbl',**e )

            # Site doesn't exisit in the database, create entry for site in the database in SiteTbl      
            else: 
                row['SiteUUID'] = uuid.uuid4()   # Add a SiteUUID for every dict in the array according to RFC 4122, uuid4 is more secure than uuid1
                logger.debug("creating UUID")
                e=valid_dictionary(row,config.SiteTbl_desc)
                mydb.write("SiteTbl",**e)

            cursor.fetchall() # Docs say you have to fetch all rows from the previous query before you do a new one 

            ####################################
            #
            # Process Assessment Informaton
            #
            ####################################
            SiteId_tbl_val = -1 # initialize with an invalid value

            # Query the database and try to find the Site mentioned actually exists in the Site Table 
            # If found get the  SiteId_tbl PK <- SiteID FK 
            cursor = mydb.select( 'SiteTbl', 'SiteId_tbl', SiteUUID=row['SiteUUID'] )
            row_results = cursor.fetchone()

            if row_results:  #We found the site
                SiteId_tbl_val = row_results[0]
            else:
                raise ValueError("Fatal: cant find SiteUUID: "+row['SiteUUID']+" in database. You must define the Site before the assessment can be entered")
                sys.exit(10)
            
            # See if the assessment is already in the database by matching the AssessmentGUID
            # If we find a matching assessment get the primary key of the match
            cursor = mydb.select( 'AssessmentResultsTbl', 'idAssessmentTable', AssessmentGUID=row['AssessmentGUID'] )
            row_results = cursor.fetchone() 
            
            if row_results:                 # We found an assessment that matches the AssessmentGUID
                idAssessmentTable_val = row_results[0]
                logger.debug( "PK:"+str(idAssessmentTable_val))
            
                # if we are authorized to overwrite the record
                if args.overwrite_assessment:
                    row['idAssessmentTable'] = idAssessmentTable_val  #Primary Key
                    logger.info("Overwriting Assessment data @ "+str(idAssessmentTable_val)+"s ...") 
                    e=valid_dictionary(row,config.AssessmentResultsTbl_desc)
                    #mydb.write("AssessmentResultsTbl",**e)
                    id = mydb.update('AssessmentResultsTbl','idAssessmentTable',row['idAssessmentTable'],**e)
                else:
                    print "Assessment exists, not updating use --overwrite_assessment to override"

            # No matching asssesment, write the new one        
            else: 
                row['SiteId'] =  SiteId_tbl_val
                logger.debug("SiteId: %d" % row['SiteId'])
                e=valid_dictionary(row,config.AssessmentResultsTbl_desc)
                mydb.write("AssessmentResultsTbl",**e)
                logger.info("Writing new asessment data ...")

            cursor.fetchall() # the docs say you need to fetch all rows before doing another query ->void
    filesProcessed.append(mfile)
logger.info("Files procesed: " + str(filesProcessed))

mydb.close()
