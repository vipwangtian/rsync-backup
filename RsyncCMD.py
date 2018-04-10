#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import datetime
import time
from BKExceptions import ArgException

class RsyncCMD(object):

    def __init__(self, job = None, rsync_conf = None):
        self.job = job
        self.rsync_conf = rsync_conf

    def build_rsync_param(self):
        param = ""
        if self.rsync_conf["archive"]:
            param += "-a "
        if self.rsync_conf["verbose"]:
            param += "-v "
        if self.rsync_conf["compress"]:
            param += "-z "
            if self.rsync_conf["compress-level"]:
                param += "--compress-level={0} ".format(self.rsync_conf["compress-level"])
        if self.rsync_conf["recursive"]:
            param += "-r "
        if self.rsync_conf["times"]:
            param += "-t "
        if self.rsync_conf["min-size"]:
            param += "--min-size={0} ".format(self.rsync_conf["min-size"])

        return param

    def resolve_datedirective(self, backup):
        date_formatter = self.rsync_conf["date-formatter"]
        directives = re.findall(r"{date(.*)}", backup)
        if len(directives):
            if directives[0].strip() != "":
                ago = int(directives[0])
            else:
                ago = 0

            if ago < 0:
                translated = (datetime.date.today() - datetime.timedelta(days=abs(ago))).strftime(date_formatter)
            else:
                translated = (datetime.date.today() + datetime.timedelta(days=abs(ago))).strftime(date_formatter)
            return re.sub(r"{date.*}", translated, backup)
        else:
            return backup

    def resolve_hostdirective(self, backup):
        return re.sub(r"{host}", self.job["host"], backup)

    def resolve_directive(self, backup):
        ret = self.resolve_datedirective(backup)
        ret = self.resolve_hostdirective(ret)
        return ret

    def get_rsync_cmd(self, job = None, rsync_conf = None):
        if job:
            self.job = job
        if rsync_conf:
            self.rsync_conf = rsync_conf
        if not self.job or not self.rsync_conf:
            raise ArgException("参数不能为空")
        param = self.build_rsync_param()
        user = self.rsync_conf["user"]
        host = self.job["host"]
        backup = self.job["backup"]
        target = self.job["target"]
        cmd = "rsync -e 'ssh' {0} {1}@{2}:{3} {4}".format(param, user, host, self.resolve_directive(backup), self.resolve_directive(target))
        return cmd
