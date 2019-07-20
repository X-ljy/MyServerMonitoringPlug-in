#coding:utf-8
'''
@auther 夕
@date 2019/5/7

'''

import commands
from time import strftime
import time
import globalvar

def getAllProcInfo():
    '''
      • USER：该进程属于那个使用者账号的？
      • PID ：该进程的进程ID号。
      • %CPU：该进程使用掉的 CPU 资源百分比；
      • %MEM：该进程所占用的物理内存百分比；
      • VSZ ：该进程使用掉的虚拟内存量 (Kbytes)
      • RSS ：该进程占用的固定的内存量 (Kbytes)
      • TTY ：该进程是在那个终端机上面运作，若与终端机无关，则显示 ?，另外， tty1-tty6 是本机上面的登入者程序，若为 pts/0 等等的，则表示为由网络连接进主机的程序。
      • STAT：该程序目前的状态，主要的状态有：
        R ：该程序目前正在运作，或者是可被运作；
        S ：该程序目前正在睡眠当中 (可说是 idle 状态啦！)，但可被某些讯号(signal) 唤醒。
        T ：该程序目前正在侦测或者是停止了；
        Z ：该程序应该已经终止，但是其父程序却无法正常的终止他，造成 zombie (疆尸) 程序的状态
      • START：该进程被触发启动的时间；
      • TIME ：该进程实际使用 CPU 运作的时间。
      • COMMAND：该程序的实际指令为什么？

      USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
      root         2  0.0  0.0      0     0 ?        S    Jun15   0:00 [kthreadd]
    '''
    allProcData = dict()
    data = dict()
    status,allProc = commands.getstatusoutput("ps -aux")
    allProc = allProc.split("\n")
    for  num in range(1,len(allProc)):
        singleProc = allProc[num].split()
        procJson = {
                   "user":singleProc[0],"pid":singleProc[1],"cpu":singleProc[2],"mem":singleProc[3],\
                   "vsz":singleProc[4],"rss":singleProc[5],"tty":singleProc[6],"status":singleProc[7],\
                   "startTime":singleProc[8]+" "+singleProc[9],"command":''.join(singleProc[10:])
                  }
        data.update({singleProc[1]:procJson})
    allProcData.update({"hostIp":globalvar.get_value("hostIp"),"date":strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),"data":data})
    return allProcData

