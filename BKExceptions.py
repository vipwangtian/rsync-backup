#!/usr/bin/env python
#-*- coding:utf-8 -*-

class ArgException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message 
