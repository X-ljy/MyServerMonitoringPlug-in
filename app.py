#coding:utf-8

'''
@auther 夕
@date 2019/5/7

'''
from bottle import route,run,template
import globalvar

import serverMonitor
import procMonitor
import mysql

# 服务器性能指标
@route("/getCpuBaseInfo",method='POST')
def getCpuBaseInfo():
    return serverMonitor.getCpuBaseInfo()

@route("/getCpuUseInfo",method='POST')
def getCpuUseInfo():
    return serverMonitor.getCpuUseInfo()

@route("/getDiskBaseInfo",method='POST')
def getDiskBaseInfo():
    return serverMonitor.getDiskBaseInfo()

@route("/getDiskIoInfo",method='POST')
def getDiskIoInfo():
    return serverMonitor.getDiskIoInfo()

@route("/getLoadAverage",method='POST')
def getLoadAverage():
    return serverMonitor.getLoadAverage()

@route("/getMemBaseInfo",method='POST')
def getMemBaseInfo():
    return serverMonitor.getMemBaseInfo()

@route("/getNetWorkCardInfo",method='POST')
def getNetWorkCardInfo():
    return serverMonitor.getNetWorkCardInfo()

@route("/getOnlineUsers",method='POST')
def getOnlineUsers():
    return serverMonitor.getOnlineUsers()

@route("/getSystemInfo",method='POST')
def getSystemInfo():
    return serverMonitor.getSystemInfo()

@route("/getAllProcInfo",method='POST')
def getAllProcInfo():
    return procMonitor.getAllProcInfo()


# mysql 性能指标
@route("/getMysqlIsAlive",method='POST')
def getMysqlIsAlive():
    return mysql.getMysqlIsAlive()

@route("/getMysqlprocesslist",method='POST')
def getMysqlprocesslist():
    return mysql.getMysqlprocesslist()

@route("/getMysqlConnectionNumber",method='POST')
def getMysqlConnectionNumber():
    return mysql.getMysqlConnectionNumber()

@route("/getMysqlUptime",method='POST')
def getMysqlUptime():
    return mysql.getMysqlUptime()

@route("/getMysqlQps",method='POST')
def getMysqlQps():
    return mysql.getMysqlQps()

@route("/getMysqlTPS",method='POST')
def getMysqlTPS():
    return mysql.getMysqlTPS()

@route("/getMysqlKeyBuffer",method='POST')
def getMysqlKeyBuffer():
    return mysql.getMysqlKeyBuffer()

@route("/getMysqlInnodbBuffer",method='POST')
def getMysqlInnodbBuffer():
    return mysql.getMysqlInnodbBuffer()

@route("/getMysqlQueryCache",method='POST')
def getMysqlQueryCache():
    return mysql.getMysqlQueryCache()    

@route("/getMysqlTableCache",method='POST')
def getMysqlTableCache():
    return mysql.getMysqlTableCache()    

@route("/getMysqlThreadCache",method='POST')
def getMysqlThreadCache():
    return mysql.getMysqlThreadCache()    

#应用接口启动
if __name__ == "__main__":
    globalvar._init()
    globalvar.set_value('mysqlUser',"root")
    globalvar.set_value("mysqlpassword","Wp60978516.")
    globalvar.set_value('hostIp',"49.82.41.170")
    run(host='0.0.0.0',port=6666)
