#!/usr/bin/env python 
# -*- coding: utf-8 -*-

###################################################################################
#
#                          Create QSF Survey Files
#
# Short Description:
# Open and parse qsf template file pull out keywords which are marked with 
#     find the equivelents in the site_file
#
# Long Description:
# Open and parse site_file an excel spread sheet create a new qsf file
# for each line of data in the site_file match it to the template and create
# a file with that data.
#
# Author: David S. Brown
# Last Major Change: 13 August 2015
#
####################################################################################


import argparse
import sys
from os import listdir, stat, mkdir
from os.path import isfile, join, splitext
from openpyxl.workbook import Workbook
from openpyxl.compat import range
from openpyxl import cell, load_workbook
import copy
import re



SUPPORTED_FORMATS = ('.xlsx', '.xlsm', '.xltx', '.xltm')
FILENAME_HEADER = 'SurveyName'

parser = argparse.ArgumentParser( description='''
                        Create QSF query files
                        ''',
                        )

####################################################################################
#
#                               Create Arguments
#
####################################################################################

# a numeric debug level as in arg_parse.py -D 3
parser.add_argument("-D", "--debug", type=int, default=0, help="Set integer debug level from 0-9 as: -D 3")


# Template File with fields to replace
parser.add_argument("-t", "--template", nargs="?", dest="template", required=True, 
                    help="qsf template file. Should be of the form file.qsf a json file")

# Excel file of fields to find the replacements in
parser.add_argument("-s", "--sites", nargs="?", dest="sites", required=True, 
                    help="Excel (.xlsx) file to read sites from")

# Directory to write to, if blank it writes to the current directory
parser.add_argument("-d", "--dir", nargs="?", dest="dir", required=True, 
                    help="Directory to write to")


# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

####################################################################################
#
#                                Functions
#
####################################################################################

def validate_excel_file(xfile):
    # returns a list of names (with extension) of all files 
    # in folder path
        if isfile(xfile) and not xfile.startswith('~'):
            (root,ext) = splitext(xfile)
            if ext in SUPPORTED_FORMATS:
                return xfile
            else:
                return ""


def get_headers(ws):
    headers=[0]
    first_row = True
    for row in ws.rows:
        for cell in row:
            if first_row:
                headers[0]+=1
                headers.append(cell.value)
            else:
                return headers
        first_row = False

def get_rows(ws):
    headers=[0]
    first_row = True
    rows = []
    for row in ws.rows:
        c = 0
        t = {}
        for cell in row:
            if first_row:
                headers[0]+=1
                headers.append(cell.value)
            else:
                 c += 1
                 t[headers[c]] = cell.value
        if first_row:
            first_row = False
            continue
        rows.append(t)
    return rows

# specialized to this program
# search string s for key + ":" until the next " 
# replace everthing between the quotes, after the key 
# with new_element and return the new string
def replace_element(s,key,new_element):
    #print "header:[%s]"%key
    st = '"%s":"'%key
    #print st
    beg = s.find(st)+len(st)
    end = s.find('"',beg)
    #print s[beg:end]
    new_s = s[:beg]+new_element+s[end:]
    return new_s

def safe_fname(s):
    keepcharacters = (' ','.','_')
    s = "".join(c for c in outfile_name if c.isalnum() or c in keepcharacters).rstrip()
    s = s.replace("  ","_")
    s = s.replace(" ","_")
    return s


####################################################################################
#
#                                   Main
#
####################################################################################


if args.debug >= 1: print "Template: [%s], Sites excel file: [%s], Optional directory: [%s]"%(args.template, args.sites, args.dir)

if isfile(args.template) and not args.template.startswith('~'):
     i = open(args.template,'r')    #It will throw an error if not opened up in U mode
     t = i.read()
     if args.debug >= 3: print t
else:
    print "Can't open %s"%args.template
    exit(2)

filename = validate_excel_file(args.sites)
if not filename:
    print "Can't find %s" % filename
    exit (1)

if args.debug >= 1: print "opening file: [%s]" % filename
wb = load_workbook(filename = filename, data_only=True)
ws = wb.get_active_sheet()
headers = get_headers(ws)
void = headers.pop(0)
for row in get_rows(ws):
    if args.debug >= 3: print row
    for k in headers:
        if not k.startswith("@@"):
            t = replace_element(t,k,row[k])
    outfile_name = row[FILENAME_HEADER]
    newdir = safe_fname(args.dir)
    if newdir:
        try:
            stat(args.dir)
        except:
            mkdir(args.dir)
        outfile_name = args.dir+"/"+safe_fname(outfile_name)+".qsf"
    o = open(outfile_name,'w') 
    o.write(t)
    o.close()