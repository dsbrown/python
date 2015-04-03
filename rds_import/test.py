#!/usr/local/bin/python
# -*- coding: utf-8 -*-



#  "INSERT INTO QuestionTbl (idQuestionTbl, QuestionnaireGUID, DocEngVersion, QuestionNo, QuestionText)  Values (%s,%s,%s,%s,%s)"


def dbwrite(table, **kwargs) :
    prefix = "INSERT INTO %s " % table
    s = "( "
    data = ()
    postfix = "VALUES ("
    for i in kwargs.keys():
        s += "%s," % i
        postfix += "%s,"
        data += (kwargs[i],) 
    s=s[:-1] # removes the final ", " 
    postfix=postfix[:-1] + ")" # removes the final ", " 
    s += ") "
    s = prefix + s + postfix



    print "SQL Statement: %s" % s, data

escaped = "Foo bar my flop flip"
d = {"QuestionTbl": 14, 'fooQuestion': 7, 'DocEngVersion': 'q_no' , 'QuestionNo': 71 , 'QuestionText' : escaped }

dbwrite('MyTable',  QuestionnaireGUID = "this string", idQuestionTbl = 42, **d )
#dbwrite('MyTable',  QuestionnaireGUID = "this string", idQuestionTbl = 42, )

