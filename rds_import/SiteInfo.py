#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from dsb_rds import *
import config  # Global Settings
import csv


# Connect to RDS

mydb = DsbRds()
mydb.connect()
mydb.create_cursor()

with open('eggtest.csv', 'wb') as csvfile:
    mywriter = csv.writer(csvfile, delimiter=',',
                          quotechar='"', quoting=csv.QUOTE_MINIMAL)

    mydb.select(
        "SiteTbl", 'SiteId_tbl', 'ClusterName', 'ClusterID', 'ProjectName',
        'AWSSiteCode', 'VendorName', 'VendorSiteName', 'VendorSiteCity',
        'VendorSiteState', 'SiteUUID',
    )

    mywriter.writerow( ['SiteId_tbl', 'ClusterName', 'ClusterID', 'ProjectName',
                       'AWSSiteCode', 'VendorName', 'VendorSiteName', 'VendorSiteCity',
                       'VendorSiteState', 'SiteUUID',] )

    row_results = mydb.get_cursor().fetchall()
    for i in row_results:
        print i
        mywriter.writerow(i)

mydb.close()




