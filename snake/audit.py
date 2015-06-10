#!/usr/local/bin/python
# -*- coding: utf-8 -*-


class Owner(object):
    ticket = {}
    desc = {}
   

    def __init__(self,owner):
        self.owner = owner
        self.ai_count = 0

    def __repr__(self):
        return "Owner object: %s"% (self.owner)

    def __str__(self):
        return self.__repr__()

    def add_ticket(self,ticket,site):
        self.ticket[ticket] = site

    def add_description(self,tt,desc):
        self.desc[tt]=desc
        self.ai_count += 1
