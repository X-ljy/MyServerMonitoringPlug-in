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

def getSystemInfo():
    '''
    获取系统信息

    {'kernelVersion': '3.10.0-957.10.1.el7.x86_64', 'RedHatVersion': 'RedHat4.8.5-36'}
        内核版本                                        红帽版本
    '''
    status,kernelVersion = commands.getstatusoutput(" cat /proc/version  | awk '{print$3}' ")
    status,RedHatVersion = commands.getstatusoutput(" cat /proc/version  | awk '{print$9$10$11}' ")
    RedHatVersion = RedHatVersion.replace("(","")
    RedHatVersion = RedHatVersion.replace(")","")
    data = {"kernelVersion":kernelVersion,"RedHatVersion":RedHatVersion} 
    return data

def getCpuBaseInfo():
    '''
    获取CPU基本信息
    {'cpuVersion': 'CPUE5-2640', 'logicCores': '1', 'cpuMHz': '2.40GHz', 'cpuName': 'Intel(R)Xeon(R)', 'PhysicsCores': '1'}
      CPU信号                         虚拟核数          CPU主频             CPU名称                        物理核数
    '''
    status,cpuName = commands.getstatusoutput(" cat /proc/cpuinfo | grep 'model name' | awk  '{print$4$5}' ")
    status,cpuVersion = commands.getstatusoutput(" cat /proc/cpuinfo | grep 'model name' | awk  '{print$6$7}' ")
    status,cpuMHz = commands.getstatusoutput(" cat /proc/cpuinfo | grep 'model name' | awk  '{print$10}' ")
    status,logicCores = commands.getstatusoutput(" cat /proc/cpuinfo | grep 'processor' | wc -l ")
    status,PhysicsCores = commands.getstatusoutput(" cat /proc/cpuinfo | grep 'cpu cores' | awk '{print$4}' ")
    cpuBaseData = {"cpuName":cpuName,"cpuVersion":cpuVersion,"cpuMHz":cpuMHz,"logicCores":logicCores,"PhysicsCores":PhysicsCores}
    return cpuBaseData

def analyData(i):
    try:
        float(i)
    except BaseException:
        i = 0.0
    return i

def getCpuUseInfo():
    '''
        us — 用户空间占用CPU的百分比。
        sy — 内核空间占用CPU的百分比。
        ni — 改变过优先级的进程占用CPU的百分比
        id — 空闲CPU百分比
        wa — IO等待占用CPU的百分比
        hi — 硬中断（Hardware IRQ）占用CPU的百分比
        si — 软中断（Software Interrupts）占用CPU的百分比
        st — 虚拟机占用百分比
    '''
    status,us = commands.getstatusoutput("top -n 1 | grep Cpu | awk '{print$2}'")
    us = analyData(us)
    status,sy = commands.getstatusoutput("top -n 1 | grep Cpu | awk '{print$4}'")
    sy = analyData(sy)
    status,ni = commands.getstatusoutput("top -n 1 | grep Cpu | awk '{print$6}'")
    ni = analyData(ni)
    status,wa = commands.getstatusoutput("top -n 1 | grep Cpu | awk '{print$10}'")
    wa = analyData(wa)
    status,hi = commands.getstatusoutput("top -n 1 | grep Cpu | awk '{print$12}'")
    hi = analyData(hi)
    status,si = commands.getstatusoutput("top -n 1 | grep Cpu | awk '{print$14}'")
    si = analyData(si)
    status,st = commands.getstatusoutput("top -n 1 | grep Cpu | awk '{print$16}'")
    st = analyData(st)
    status,id = commands.getstatusoutput("top -n 1 | grep Cpu | awk '{print$8}'")
    try:
        float(id)
    except BaseException:
        id = 100 - float(us) - float(sy)
    cpuUseData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"us":us,\
                            "sy":sy,"ni":ni,"id":id,"wa":wa,"hi":hi,"si":si,"st":st}
    return cpuUseData

def getMemBaseInfo():
    '''
        memTotal — 物理内存总量
        memUsed — 使用中的内存总量
        memFree — 空闲内存总量
        memCache — 缓存的内存量 

        swapTotal — 交换区总量
        swapUsed — 使用的交换区总量
        swapFree — 空闲交换区总量
        swapCache — 缓冲的交换区总量
    '''
    memData = dict()
    status,memTotal = commands.getstatusoutput("top -n 1 | grep 'KiB Mem'  | awk '{print$4}'")
    status,memFree = commands.getstatusoutput("top -n 1 | grep 'KiB Mem'  | awk '{print$6}'")
    status,memUsed = commands.getstatusoutput("top -n 1 | grep 'KiB Mem'  | awk '{print$8}'")
    status,memCache = commands.getstatusoutput("top -n 1 | grep 'KiB Mem'  | awk '{print$10}'")
    status,swapTotal = commands.getstatusoutput("top -n 1 | grep 'KiB Swap'  | awk '{print$3}'")
    status,swapFree = commands.getstatusoutput("top -n 1 | grep 'KiB Swap'  | awk '{print$5}'")
    status,swapUsed = commands.getstatusoutput("top -n 1 | grep 'KiB Swap'  | awk '{print$7}'")
    status,swapCache = commands.getstatusoutput("top -n 1 | grep 'KiB Swap'  | awk '{print$9}'")
    temp = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"memTotal":memTotal,\
            "memFree":memFree,"memUsed":memUsed,"memCache":memCache,"swapTotal":swapTotal,\
            "swapFree":swapFree,"swapUsed":swapUsed,"swapCache":swapCache}
    memData.update({"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"data":temp})
    return memData

def getDiskBaseInfo():
    '''
        Filesystem：代表该文件系统时哪个分区，所以列出的是设备名称。
        Size：空间总大小
        Used：已经使用的空间大小。
        Available：剩余的空间大小。
        Use%：磁盘使用率。如果使用率在90%以上时，就需要注意了，避免磁盘容量不足出现系统问题，尤其是对于文件内容增加较快的情况(如/home、/var/spool/mail等)。
        Mounted on：磁盘挂载的目录，即该磁盘挂载到了哪个目录下面
    '''
    allDiskData = dict()
    data = dict()
    status,diskList = commands.getstatusoutput("df -h")
    diskList = diskList.split("\n")
    for i  in  range(1,len(diskList)):
        diskInfo = diskList[i].split()
        temp = {"fileSystem":diskInfo[0],"diskSize":diskInfo[1],"diskUsed":diskInfo[2],\
                     "diskAvail":diskInfo[3],"diskUseRate":diskInfo[4],"mounted":diskInfo[5]} 
        data.update({diskInfo[0]:temp})
    allDiskData.update({"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"data":data})
    return allDiskData                 

    
def getDiskIoInfo():
    '''
        rrqm/s:  每秒进行 merge 的读操作数目。即 rmerge/s
        wrqm/s:  每秒进行 merge 的写操作数目。即 wmerge/s
        r/s:  每秒完成的读 I/O 设备次数。即 rio/s
        w/s:  每秒完成的写 I/O 设备次数。即 wio/s
        rkB/s:  每秒读K字节数。是 rsect/s 的一半，因为每扇区大小为512字节。
        wkB/s:  每秒写K字节数。是 wsect/s 的一半。
        avgrq-sz:  平均每次设备I/O操作的数据大小 (扇区)。
        avgqu-sz:  平均I/O队列长度。
        await: 平均每次设备I/O操作的等待时间 (毫秒)。
        r_await:每个读操作平均所需的时间,不仅包括硬盘设备读操作的时间，还包括了在kernel队列中等待的时间。
        w_await:每个写操作平均所需的时间,不仅包括硬盘设备写操作的时间，还包括了在kernel队列中等待的时间。
        svctm: 平均每次设备I/O操作的服务时间 (毫秒)。
        %util:  一秒中有百分之多少的时间用于 I/O 操作，即被io消耗的cpu百分比
    '''
    allDeviceData = dict()
    deviceData = dict()
    status,deviceList = commands.getstatusoutput("iostat -d -x -k 1 1 | awk '{print$1}'")
    deviceList = deviceList.split("\n")
    for num in range(3,len(deviceList)):
        if deviceList[num] == '':
            continue
        else:
            status,rmerge = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$2}'")
            status,wmerge = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$3}'")
            status,rio = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$4}'")
            status,wio = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$5}'")
            status,rkB = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$6}'")
            status,wkB = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$7}'")
            status,avgrqsz = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$8}'")
            status,avgqusz = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$9}'")
            status,await = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$10}'")
            status,r_await = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$11}'")
            status,w_await = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$12}'")
            status,svctm = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$13}'")
            status,util = commands.getstatusoutput("iostat -d -x -k 1 1 | grep "+ deviceList[num] +" | awk '{print$14}'")
            singleDeviceData = dict()
            singleDeviceData.update({"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"rmerge":rmerge,"wmerge":wmerge,"rio":rio,"wio":wio,"rkB":rkB,"wkB":wkB,"avgrqsz":avgrqsz,\
                                     "avgqusz":avgqusz,"await":await,"r_await":r_await,"w_await":w_await,"svctm":svctm,"util":util})
            allDeviceData.update({deviceList[num]:singleDeviceData})
    deviceData.update({"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"data":allDeviceData})
    return deviceData        

def getLoadAverage():
    '''
    平均负载
    load average: 0.09,   0.04,   0.05
                1minute  5minute 15minute
    '''
    status,data = commands.getstatusoutput(" top -n 1 | grep 'load average' ")
    data = data[data.rfind('load average:'):]
    data = data.split()
    oneLoadAverage = data[2].replace(',','')
    fiveLoadAverage = data[3].replace(',','')
    temp = str(data[4])
    fifteenLoadAverage = temp[0:4]
    loadAverageData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"oneLoadAverage":oneLoadAverage,"fiveLoadAverage":fiveLoadAverage,"fifteenLoadAverage":fifteenLoadAverage}
    return loadAverageData;

def getNetWorkCardInfo():
    '''
        IFACE：就是网络设备的名称
        rxpck/s：每秒钟接收到的包数目
        txpck/s：每秒钟发送出去的包数目
        rxkB/s：每秒钟接收到的字节数
        txkB/s：每秒钟发送出去的字节数
        rxcmp/s：每秒钟接收到的压缩包数目
        txcmp/s：每秒钟发送出去的压缩包数目
        txmcst/s：每秒钟接收到的多播包的包数目
    '''
    allNetworkData = dict()
    data = dict()
    status,allNetworkInfo = commands.getstatusoutput("sar -n DEV 1 1 | grep Average")
    allNetworkInfo = allNetworkInfo.split("\n")
    for i in range(1,len(allNetworkInfo)):
        singleNetworkData = allNetworkInfo[i].split()
        singleNetWorkJson = {
                     "iface":singleNetworkData[1],"rxpck":singleNetworkData[2],"txpck":singleNetworkData[3],\
                     "rxkB":singleNetworkData[4],"txkB":singleNetworkData[5],"rxcmp":singleNetworkData[6],\
                     "txcmp":singleNetworkData[7],"txmcst":singleNetworkData[8]
                    }
        data.update({singleNetworkData[1]:singleNetWorkJson})
    allNetworkData.update({"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"data":data})
    return allNetworkData

def getOnlineUsers():
    '''
    获取在线用户信息
    USER     TTY      FROM             LOGIN@   IDLE         JCPU                           PCPU            WHAT
    root     pts/1    121.69.12.189    10:05   19:59         1.08s                         1.07s           python
                                            用户空闲时间 和终端连接所有进程占用时间        当前进程占用时间    操作命令
    '''
    data = list()
    status,allUserInfo = commands.getstatusoutput("w -h")
    allUserInfo = allUserInfo.split("\n")   
    for i in range(0,len(allUserInfo)):
        sigleUserData = allUserInfo[i].split()
        sigleUserData[7] = ''.join(sigleUserData[7:])
        data.append(sigleUserData)
    allUserData = {"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"data":data}
    return allUserData
