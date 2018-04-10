#!/usr/bin/env python
#-*- coding:utf-8 -*-

import yaml
import os
from BKExceptions import ConfException

class BakConfig(object):
    yaml_path = "conf/config.yaml"

    def __init__(self):
        f = open(self.yaml_path ,'r')
        conf = f.read()
        f.close()
        self.yaml_conf = yaml.load(conf)

    def __check_conf(self):
        pass

    def get_jobs(self):
        if self.yaml_conf:
            jobs = self.yaml_conf["JOB"]
            return sorted(jobs, key=lambda job:job["priority"], reverse=True)
        else:
            raise ConfException("配置文件异常")

    def get_rsync_conf(self):
        if self.yaml_conf:
            return self.yaml_conf["RSYNC"]
        else:
            raise ConfException("配置文件异常")