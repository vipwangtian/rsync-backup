#!/usr/bin/env python
#-*- coding:utf-8 -*-

import yaml
import os

class BakConfig(object):
    yaml_path = "conf/config.yaml"

    def __init__(self):
        f = open(self.yaml_path ,'r')
        conf = f.read()
        f.close()
        self.yaml_conf = yaml.load(conf)

    def get_jobs(self):
        return self.yaml_conf["JOB"]

    def get_rsync_conf(self):
        return self.yaml_conf["RSYNC"]