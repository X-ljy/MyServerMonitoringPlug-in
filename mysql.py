#coding:utf-8
'''
@auther 夕
@date 2019/5/7
'''

import commands
from time import strftime
import time

#引入全局变量管理模块
import globalvar



def getMysqlIsAlive():
    '''
    查看mysql是否alive
    '''
    status,isAlive = commands.getstatusoutput("mysqladmin -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  +" -h localhost ping")
    if "alive" in isAlive:
        return "alive"
    else:
        return "not alive"

def getMysqlprocesslist():
    '''
    获取数据库当前连接信息
    | Id  | User | Host      | db | Command | Time | State    | Info             |
    +-----+------+-----------+----+---------+------+----------+------------------+
    | 136 | root | localhost |    | Query   | 0    | starting | show processlist |
    '''
    data = dict()
    status,processlist = commands.getstatusoutput("mysqladmin -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  +" -h localhost processlist")
    processlist = processlist.split("\n")
    if(len(processlist) > 4):
        for i in range(4,len(processlist)-1,1):     
            temp = processlist[i].split("|")
            id = temp[1]
            user = temp[2]
            host = temp[3]
            db = temp[4]
            command = temp[5]
            Time = temp[6]
            state = temp[7]
            info = temp[8]
            
            datatemp = {"id":id,"user":user,"host":host,"db":db,"command":command,"time":Time,"state":state,"info":info}
            data.update({id:datatemp})
    
    processlistData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"data":data}
    return processlistData

def getMysqlConnectionNumber():
    '''
        获取当前连接数
        +-----------+-------------+
        | host      | count(host) |
        +-----------+-------------+
        | localhost |           1 |
        +-----------+-------------+
    '''
    data = dict()
    status,connectionlist = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
        +' -hlocalhost -e \"select host,count(host) from processlist group by host;\" information_schema')
    connectionlist = connectionlist.split("\n")
    if(len(connectionlist) > 2):
        for i in range(2,len(connectionlist),1):     
            temp = connectionlist[i].split("\t")
            host = temp[0]
            count = temp[1]
            datatemp = {"host":host,"count":count}
            data.update({host:datatemp})
    connectionNumberData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"data":data}
    return connectionNumberData

def getMysqlUptime():
    '''
        获取mysql的uptime
        Uptime 1.205Hour
        Uptime_since_flush_status 1.205Hour
    '''
    status,upTime = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost' + "  -e  \" SHOW STATUS LIKE \'%uptime%\' \"  |  awk \'/ptime/{ calc = $NF / 3600;print $(NF-1), calc\"Hour\" }\' ")
    upTime = upTime.split("\n");
    upTimeData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),\
        "Uptime":upTime[1].split(" ")[1],"Uptime_since_flush_status":upTime[2].split(" ")[1]}
    return upTimeData


def getMysqlQps():
    '''
        获取mysql qps
        QPS的计算方法
        QPS:每秒的查询数
        Questions = SHOW GLOBAL STATUS LIKE 'Questions';
        Uptime = SHOW GLOBAL STATUS LIKE 'Uptime';
        QPS=Questions/Uptime
    '''
    status,Questions  = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\" SHOW GLOBAL STATUS LIKE 'Questions'; \"")
    status,Uptime   = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\" SHOW GLOBAL STATUS LIKE 'Uptime'; \"")

    Questions = Questions.split("\n")
    Questionsdata = Questions[2].split("\t")[1]

    Uptime = Uptime.split("\n")
    Uptimedata = Uptime[2].split("\t")[1]

    QPS = float(Questionsdata)/float(Uptimedata)
    qpsData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"qps":round(QPS,3)}    
    return qpsData

def getMysqlTPS():
    '''
        TPS的计算方法
        Com_commit = SHOW GLOBAL STATUS LIKE 'Com_commit';
        Com_rollback = SHOW GLOBAL STATUS LIKE 'Com_rollback';
        Uptime = SHOW GLOBAL STATUS LIKE 'Uptime';
        TPS=(Com_commit + Com_rollback)/Uptime
    '''
    status,Com_commit = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\" SHOW GLOBAL STATUS LIKE 'Com_commit'; \"")
    
    status,Com_rollback  = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\" SHOW GLOBAL STATUS LIKE 'Com_rollback'; \"")

    status,Uptime = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\" SHOW GLOBAL STATUS LIKE 'Uptime'; \"")

    Com_commit = Com_commit.split("\n")
    Com_commit = Com_commit[2].split("\t")[1]    

    Com_rollback = Com_rollback.split("\n")
    Com_rollback = Com_rollback[2].split("\t")[1]    

    Uptime = Uptime.split("\n")
    Uptime = Uptime[2].split("\t")[1]

    TPS = ( float(Com_commit) + float(Com_commit) )/float(Uptime)
    tpsData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"tps":round(TPS,3)}       
    return tpsData

def getMysqlKeyBuffer():
    '''
        获取mysql Key Buffer 命中率
        mysql Key Buffer 命中率 
        key_buffer_read_hits = (1 - Key_reads / Key_read_requests) * 100% 
        key_buffer_write_hits= (1 - Key_writes / Key_write_requests) * 100% 
    '''
    status,data = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\"show global status like 'key_read%';\"")
    data = data.split("\n")
    Key_reads = data[3].split("\t")[1]
    Key_read_requests = data[2].split("\t")[1]
    key_buffer_read_hits = 1 - float(Key_reads)/float(Key_read_requests)

    status,data = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\"show global status like 'key_write%';\"")
    data = data.split("\n")
    Key_writes = data[2].split("\t")[1]
    Key_write_requests = data[2].split("\t")[1]

    if Key_write_requests == '0':
        key_buffer_write_hits = 1
    else:
        key_buffer_write_hits = 1 - float(Key_writes)/float(Key_write_requests)

    KeyBufferData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"key_buffer_read_hits":round(key_buffer_read_hits,3),"key_buffer_write_hits":round(key_buffer_write_hits,3)}
    return KeyBufferData

def getMysqlInnodbBuffer():
    '''
    #mysql Innodb Buffer 命中率
    innodb_buffer_read_hits=(1-Innodb_buffer_pool_reads/Innodb_buffer_pool_read_requests) * 100% 

    '''
    status,data = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\"show global status like 'Innodb_buffer_pool_read%';\"")
    data = data.split("\n")
    Innodb_buffer_pool_reads = data[6].split("\t")[1]
    Innodb_buffer_pool_read_requests = data[5].split("\t")[1]

    if Innodb_buffer_pool_read_requests == '0':
        innodb_buffer_read_hits = 1
    else:
        innodb_buffer_read_hits = 1 - float(Innodb_buffer_pool_reads)/float(Innodb_buffer_pool_read_requests)

    InnodbBufferData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"innodb_buffer_read_hits":round(innodb_buffer_read_hits,3)}
    return InnodbBufferData

def getMysqlQueryCache():
    '''
        #mysql Query Cache 命中率
        Query_cache_hits= (Qcache_hits / (Qcache_hits + Qcache_inserts)) * 100%
    '''
    status,data = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\"show global status like 'Qcache%';\"")
    
    data = data.split("\n")

    Qcache_hits = data[4].split("\t")[1]
    Qcache_inserts = data[5].split("\t")[1]
    
    if int(Qcache_inserts) + int(Qcache_hits) == 0:
        Query_cache_hits = 1
    else:
        Query_cache_hits= ( float(Qcache_hits) / ( float(Qcache_hits) + float(Qcache_inserts)))
    QueryCacheData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"Query_cache_hits":round(Query_cache_hits,3)}
    return QueryCacheData

def getMysqlTableCache():
    '''
        mysql Table Cache 状态量
        Open_files  ：代表当前打开的文件
        Opened_files ：代表使用MySQL的my_open()函数打开过的文件数。
        Opened_table_definitions ：代表自从MySQL启动后，缓存了.frm文件的数量。
        Open_table_definitions  ：代表当前缓存了多少.frm文件。
        Opened_tables ：代表自从MySQL启动后，打开表的数量。
        Open_tables  ：代表当前打开表的数量。
    '''
    status,data = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\"show global status like 'Open%';\"")
    data = data.split("\n")
    
    Open_files = data[2].split("\t")[1]
    Opened_files = data[6].split("\t")[1]
    Opened_table_definitions = data[7].split("\t")[1]
    Open_table_definitions = data[4].split("\t")[1]
    Opened_tables = data[8].split("\t")[1]
    Open_tables = data[5].split("\t")[1]
    TableCacheData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),\
                      "Open_files":Open_files,"Opened_files":Opened_files,"Opened_table_definitions":Opened_table_definitions,\
                      "Open_table_definitions":Open_table_definitions,"Opened_tables":Opened_tables,"Open_tables":Open_tables}
    return TableCacheData

def getMysqlThreadCache():
    '''
        #mysql Thread Cache 命中率  
        Thread_cache_hits = (1 - Threads_created / Threads_connected*100) * 100%  
        正常来说,Thread Cache 命中率要在 90% 以上才算比较合理
    '''
    status,data = commands.getstatusoutput("mysql -u"+ str(globalvar.get_value('mysqlUser')) +" -p"+ str(globalvar.get_value('mysqlpassword'))  \
            +' -hlocalhost -e ' + "\"show global status like 'Thread%';\"")

    data = data.split("\n")
    Threads_created = data[4].split("\t")[1]
    Threads_connected = data[3].split("\t")[1]
    Thread_cache_hits = 1 - float(Threads_created)/(float(Threads_connected)*100)

    ThreadCacheData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"Thread_cache_hits":round(Thread_cache_hits,3)}

    return ThreadCacheData



