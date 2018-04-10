#!/usr/bin/env python
#-*- coding:utf-8 -*-

import yaml
import os
import time
import datetime
import json
import traceback
from BakConfig import BakConfig 
from RsyncCMD import RsyncCMD
from common.cmds import cmds

class RsyncBackup(object):

    def __init__(self):
        self.bakConfig = BakConfig()
        self.jobs = self.bakConfig.get_jobs()
        self.rsync_conf = self.bakConfig.get_rsync_conf()
        self.rsync = RsyncCMD()

    def backup(self):
        results = []
        for job in self.jobs:
            try:
                cmd_str = self.rsync.get_rsync_cmd(job = job, rsync_conf = self.rsync_conf)
                begin = { "job" : job, "cmd_str" : cmd_str, "begin_time" : time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) }
                cmd = cmds(cmd_str)
                end = { "std_output" : cmd.stdo(), "code" : cmd.code(), "std_error" : cmd.stde(), "end_time" : time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) }
                results.append(dict(begin, **end))
            except Exception as e:
                print(job.name + " execute error!")
                tb = traceback.format_exc()
                print(tb)
        return results

    def save_result(self, results):
        date_formatter = self.rsync_conf["date-formatter"]
        html_dir = self.rsync_conf["result-dir"].strip().rstrip("/")
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)
        with open("{0}/{1}.json".format(html_dir, datetime.date.today().strftime(date_formatter)), 'w') as f:
            f.write(json.dumps(results))

if __name__ == "__main__":
    try:
        rsync = RsyncBackup()
        results = rsync.backup()
        rsync.save_result(results)
        print(results)
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
