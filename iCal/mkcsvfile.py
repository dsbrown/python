#!/usr/local/bin/python
# -*- coding: utf-8 -*-

outfile = "output.csv"
QUOTE='"'
DELIM_FIELD = ","
DELIM_ROW   = "\n"
#DATE_FORMAT = "%d.%m.%Y"



#"Subject", "Start Date", "Start Time", "End Date", "End Time", "All Day Event", "Description", "Location", "Private"
#“Start Date” and “End Date” must be in MM/DD/YYYY
# “Start Time” and “End Time” can be either 24 hour time (13:45) or 12 AM/PM (01:45 PM)
# “All Day Event” is evaluated on a “True” / “False” basis.
# “Private” is another “True” / “False”

fp = open(outfile,'wb')
fp.write(QUOTE)
fp.write("Subject")
fp.write(QUOTE)
fp.write(DELIM_FIELD)
fp.write(QUOTE)
fp.write("Start Date")
fp.write(QUOTE)
fp.write(DELIM_FIELD)
fp.write(QUOTE)
fp.write("Start Time")
fp.write(QUOTE)
fp.write(DELIM_FIELD)
fp.write(QUOTE)
fp.write("End Date")
fp.write(QUOTE)
fp.write(DELIM_FIELD)
fp.write(QUOTE)
fp.write("End Time")
fp.write(QUOTE)
fp.write(DELIM_FIELD)
fp.write(QUOTE)
fp.write("All Day Event")
fp.write(QUOTE)
fp.write(DELIM_FIELD)
fp.write(QUOTE)
fp.write("Description")
fp.write(QUOTE)
fp.write(DELIM_FIELD)
fp.write(QUOTE)
fp.write("Location")
fp.write(QUOTE)
fp.write(DELIM_FIELD)
fp.write(QUOTE)
fp.write("Private")
fp.write(QUOTE)
fp.write(DELIM_ROW)


fp.close()