
####################################################################################
#
#                                   Module
# Description:
#
#    DsbRds - AWS RDS Data Base Interface Module
#    Connects to MySql RDS Database and performs standard SELECT INSERT DELETE 
#
#    Builds 'pythonic'(TM) queries using %s string expansion to ensure variables
#    Are converted and quack appropriatly
#
# Author: David S. Brown
# v1.0  DSB      4 Apr 2015     Created
# v1.1  DSB      7 Apr 2015     Added compoud search function
#
####################################################################################

import sys
import config  # Global Settings
import boto.rds
import MySQLdb

####################################################################################
#
# USAGE:
# first, connect to RDS thusly:
#   mydb = DsbRds()
#   mydb.connect()
#   mydb.create_cursor()
# then, call the appropiate functions
# see comments below for: build_clear, build_search, build_search_or, search_execute
####################################################################################


class DsbRds(object):
    aws_region = config.aws_region
    db_instance = config.db_instance
    db_user = config.db_user
    db_password = config.db_password
    db_name = config.db_name
    conn = ""
    endpoint = ""
    mydb = ""
    cursor = ""
    data =[]
    query = ""
    count = -1

    def __init__(self):
        pass

    def __repr__(self):
        return "AWS Region: %s\n, Connection: %s\n, RDS endpoint: %s\n, RDS Instance: %s\n, AWS user: %s\n, RDS Name: %s\n, RDS MYSQL DB: %s\n " \
        % (self.aws_region, self.conn, self.endpoint, self.db_instance, self.db_user, self.db_name, self.mydb)

    def __str__(self):
        return self.__repr__()

    def connect(self):
        self.conn = boto.rds.connect_to_region(self.aws_region)
        instances = self.conn.get_all_dbinstances()
        instance = self.conn.get_all_dbinstances(self.db_instance)
        db = instance[0]
        self.endpoint,self.port = db.endpoint
        self.mydb=MySQLdb.connect(host=self.endpoint,user=self.db_user,passwd=self.db_password,db=self.db_name,port=self.port)
        return self.mydb

    def create_cursor(self):
        self.cursor = self.mydb.cursor()
        self.cursor.execute("SET NAMES 'utf8'") # forces connection to UTF-8
        return(self.cursor)

    def get_cursor(self):
        try:
            self.cursor
        except:
            print "You must create cursor first before you use it"
        else:
            return self.cursor 

    def connector(self):
        try:
            self.mydb
        except:
            print "You must connect to the database before you use it"
        else:
            return self.mydb

    def escape_string(self,text):
        return self.mydb.escape_string(text)

    def close(self):
        self.cursor.close()
        self.mydb.close()
        self.conn.close()

    def commit(self):
        self.mydb.commit()

    def write(self, table, **kwargs) :
        prefix = "INSERT INTO %s " % table
        s = "( "
        data = ()
        postfix = "VALUES ("
        for i in kwargs.keys():
            s += "%s," % i
            postfix += "%s,"
            data += (kwargs[i],) 
        s=s[:-1] # removes the final "," 
        postfix=postfix[:-1] + ")" # removes the final "," 
        s += ") "
        s = prefix + s + postfix
     
        try:
            print "SQL Statement: %s" % s
            print "Data: "
            print data
            affected_count = self.cursor.execute(s, data)
            #print "Wrote %s records " % str(affected_count)
            self.commit()
            return affected_count

        except MySQLdb.Error, e:
            print ( "write: Error failed to write %d: %s" % (e.args[0], e.args[1]))
            sys.exit (10)

    # When you have a foriegn key constraint you can't simply delete and write a record to replace it.
    # mysql offers an UPDATE or REPLACE function that provides this functionality, this is a non-standard
    # functionality but much handier then walking through the records and rebuilding the foreign keys
    # Here we implement UPDATE, if  you switch databases you will need to re-implement it in the new database
    # capability, or walk the tables and columns which will be u-g-l-y
    #
    # pk_name is the column name for the primary key in the table
    # pk_value is the primary key value you want to update
    # example: id = mydb.update('Table1',pk,**dictonary)
    def update(self, table, pk_name, pk_value, **kwargs) :
        prefix = "UPDATE %s SET " % table
        s = ""
        data = ()

        for i in kwargs.keys():
            s += "%s = " % i
            s += " %s, "
            data += (kwargs[i],) 
        s=s[:-2] # removes the final "," 
        postfix = " WHERE %s = " % pk_name
        postfix += " %s "
        data += (pk_value,)
        s = prefix + s + postfix
     
        try:
            #print "SQL Statement: %s (%s)" % (s, data)
            count = -1
            count = self.cursor.execute(s, data)
            #print "Wrote %d records " % count
            self.commit()
            return count

        except MySQLdb.Error, e:
            print ( "update: Error failed to write %d: %s" % (e.args[0], e.args[1]))
            sys.exit (10)

    # DELETE FROM QuestionTbl WHERE idQuestionTbl=%s" 
    def delete(self, table, **kwargs) :
        prefix = "DELETE FROM %s WHERE " % table
        s = " "
        data = ()
        for i in kwargs.keys():
            s += "%s=" % i
            s += "%s AND "
            data += (kwargs[i],) 
        s=s[:-4]                    # removes the final " AND " 
        s = prefix + s 
     
        try:
            #print ("SQL Statement: %s", s)
            affected_count = self.cursor.execute(s, data)
            self.commit()
            #print ("Deleted %s records ",str(affected_count))
            return affected_count

        except MySQLdb.Error, e:
            print ( "delete: Error failed to write %d: %s" %( e.args[0], e.args[1]))
            sys.exit (10)

    # SELECT idQuestionTbl, QuestionNo FROM QuestionTbl WHERE QuestionnaireGUID = %s"
    def select(self, table, *columns, **kwargs) :
        prefix = "SELECT "
        s = ""
        data = ()

        for i in columns:
            #print "columns: %s" % i
            s += "%s," % i

        s=s[:-1]
        s += " FROM %s WHERE " % table     

        for i in kwargs.keys():
            s += "%s=" % i
            s += "%s AND "
            data += (kwargs[i],) 
        s=s[:-4]                    # removes the final " AND " 
        s = prefix + s 
     
        try:
            #print ("SQL Statement: %s", s)
            self.count = self.cursor.execute(s, data)
            #print ("Selected records ",str(affected_count))
            return self.cursor

        except MySQLdb.Error, e:
            print  "select: Error failed to select %d: %s" % e.args[0], e.args[1]

    # These public functions:
    #
    #       build_clear, build_search, build_search_or, search_execute
    #
    # are used to build compound queries of the form:
    # SELECT col1,...coln FROM table1 WHERE kwargs1=%s1 AND kwargs2=%s,...,kwargsn=%sn, (data to fill in all %s) 
    # for example:
    # SELECT SiteId_tbl,SiteUUID FROM SiteTbl WHERE A=%s AND B=%s  OR (C=%s AND D=%s AND E=%s) ('166', '-77', 'McMurdo Station', 'Antarctica', '234')
    # You do this by
    # 1) build_search - creates the SELECT col1,...coln FROM table1 WHERE A=%s AND B=%s portion
    # 2) build_search_or - creates the OR (C=%s AND D=%s AND E=%s)
    # 3) search_execute - does the actual mysql search and returns a MySQLdb get_cursor
    # 

    def build_clear(self):
        self.query = ""
        self.data = ()
    
    # then hold all variables here in this module instead of all this crazy passing.

    def build_search(self, table, columns, kwargs) :
        self.build_clear()

        self.query= "SELECT "
        for i in columns:
            self.query+= "%s," % i
        self.query=self.query[:-1]
        self.query+= " FROM %s WHERE " % table     

        for i in kwargs.keys():
            self.query+= "%s=" % i
            self.query+= "%s AND "
            self.data += (kwargs[i],) 
        self.query=self.query[:-4]                    # removes the final " AND " 

    def build_search_or(self,kwargs):
        s = ""
        for i in kwargs.keys():
            #print i
            s+= "%s=" % i
            s+= "%s AND "
            self.data+= (kwargs[i],) 
        s=s[:-4]                    # removes the final " AND " 
        self.query+= " OR (" + s+ ")"

    def search_execute(self):
        try:
            #print "search_execute: %s %s" % (self.query,str(self.data))
            self.count = self.cursor.execute(self.query, self.data)
            #print "Number of records :%d" % self.count
            return self.cursor
        except MySQLdb.Error, e:
            print ( "search_execute: Error failed to select %d: %s  - SQL:%s (%s)" , e.args[0], e.args[1], self.query, self.data)
