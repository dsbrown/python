
import sys
import config  # Global Settings
import boto.rds
import MySQLdb

class Dsb_rds(object):
    aws_region = config.aws_region
    db_instance = config.db_instance
    db_user = config.db_user
    db_password = config.db_password
    db_name = config.db_name
    conn = ""
    endpoint = ""
    mydb = ""
    cursor = ""


    def __init__(self):
        pass

    def __repr__(self):
        return "Future debugging %s" % (self.aws_region)

    def __str__(self):
        return self.__repr__()

    def dbconnect(self):
        self.conn = boto.rds.connect_to_region(self.aws_region)
        instances = self.conn.get_all_dbinstances()
        #logger.debug( "Instances: " + str(instances))
        instance = self.conn.get_all_dbinstances(self.db_instance)
        db = instance[0]
        self.endpoint,self.port = db.endpoint
        #logger.debug(  "endpoint [" + str(self.endpoint) + " " + str(self.port) + "]")
        #logger.debug(  "Connecting to MySQL using MySQLdb: "+ "host="+self.endpoint+","+"user="+self.db_user+","+"passwd="+self.db_password+","+"db="+self.db_name+","+"port="+str(self.port) )
        self.mydb=MySQLdb.connect(host=self.endpoint,user=self.db_user,passwd=self.db_password,db=self.db_name,port=self.port)
        return self.mydb

    def db_create_cursor(self):
        self.cursor = self.mydb.cursor()
        self.cursor.execute("SET NAMES 'utf8'") # forces connection to UTF-8
        return(self.cursor)

    def db_cursor(self):
        try:
            self.cursor
        except:
            print "You must create cursor first before you use it"
        else:
            return self.cursor 

    def db_connector(self):
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

    def dbwrite(self, table, **kwargs) :
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
            #print ("SQL Statement: %s", s)
            affected_count = self.cursor.execute(s, data)
            #print ("Wrote %s records ",str(affected_count))
            return affected_count

        except MySQLdb.Error, e:
            print ( "dbwrite: Error failed to write %d: %s" , e.args[0], e.args[1])
            sys.exit (10)

    # DELETE FROM QuestionTbl WHERE idQuestionTbl=%s" 
    def dbdelete(self, table, **kwargs) :
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
            #print ("Deleted %s records ",str(affected_count))
            return affected_count

        except MySQLdb.Error, e:
            print ( "dbwrite: Error failed to write %d: %s" , e.args[0], e.args[1])
            sys.exit (10)

    # SELECT idQuestionTbl, QuestionNo FROM QuestionTbl WHERE QuestionnaireGUID = %s"
    def dbselect(self, table, *columns, **kwargs) :
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
            affected_count = self.cursor.execute(s, data)
            #print ("Selected records ",str(affected_count))
            return self.cursor

        except MySQLdb.Error, e:
            print ( "dbselect: Error failed to select %d: %s" , e.args[0], e.args[1])

