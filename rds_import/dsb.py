
import sys
import config  # Global Settings
import boto.rds
import MySQLdb

def dbconnect(aws_region,db_instance,db_user,db_password,db_name):
    conn = boto.rds.connect_to_region(aws_region)
    instances = conn.get_all_dbinstances()
    #logger.debug( "Instances: " + str(instances))
    instance = conn.get_all_dbinstances(db_instance)
    db = instance[0]
    endpoint,port = db.endpoint
    #logger.debug(  "endpoint [" + str(endpoint) + " " + str(port) + "]")
    #logger.debug(  "Connecting to MySQL using MySQLdb: "+ "host="+endpoint+","+"user="+db_user+","+"passwd="+db_password+","+"db="+db_name+","+"port="+str(port) )
    mydb=MySQLdb.connect(host=endpoint,user=db_user,passwd=db_password,db=config.db_name,port=port)
    return(conn, mydb)

def dbcursor(mydb):
    cursor = mydb.cursor()
    cursor.execute("SET NAMES 'utf8'") # forces connection to UTF-8
    return(cursor)

def dbwrite(cursor, table, **kwargs) :
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
        affected_count = cursor.execute(s, data)
        #print ("Wrote %s records ",str(affected_count))
        return affected_count

    except MySQLdb.Error, e:
        print ( "dbwrite: Error failed to write %d: %s" , e.args[0], e.args[1])
        sys.exit (10)

# DELETE FROM QuestionTbl WHERE idQuestionTbl=%s" 
def dbdelete(cursor, table, **kwargs) :
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
        affected_count = cursor.execute(s, data)
        #print ("Deleted %s records ",str(affected_count))
        return affected_count

    except MySQLdb.Error, e:
        print ( "dbwrite: Error failed to write %d: %s" , e.args[0], e.args[1])
        sys.exit (10)`

# SELECT idQuestionTbl, QuestionNo FROM QuestionTbl WHERE QuestionnaireGUID = %s"
def dbselect(cursor, table, *columns, **kwargs) :
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
        affected_count = cursor.execute(s, data)
        #print ("Selected records ",str(affected_count))
        return cursor

    except MySQLdb.Error, e:
        print ( "dbselect: Error failed to select %d: %s" , e.args[0], e.args[1])

