#!/usr/bin/env python3

import argparse
import json
import numpy
import os
import random
import re
import subprocess
import sys
import time
import datetime
from collections import OrderedDict
args = None
logFile = None
balanceFile = None

unlockTimeout = 999999999


def now():
    now_time = datetime.datetime.now()
    time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return time
    

def run(args):
    logFile.write(args + '\n')
    if subprocess.call(args, shell=True):
        print('bios-boot-tutorial.py: exiting because of error')

def runnotlog(args):
    subprocess.call(args, shell=True)
        
def sleep(t):
    print('sleep', t, '...')
    time.sleep(t)
    print('resume')


def getPlayer(name):
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    cmd = args.cleos + 'get table eosknightsio eosknightsio player -L ' + name + " -U " + name +'a'+ ' > '+filename
    subprocess.call(cmd, shell=True)
    time.sleep(1)
    with open(filename) as f:
        try:
            result = json.load(f)
        except:
            return -1
        subprocess.call('rm -f '+filename, shell=True)
        last_rebirth=result['rows'][0]['last_rebirth']
        return last_rebirth

def getAliveSec(name):
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    cmd = args.cleos + 'get table eosknightsio eosknightsio knight -L ' + name + " -U " + name +'a'+ ' > '+filename
    subprocess.call(cmd, shell=True)
    time.sleep(1)
    with open(filename) as f:
        try:
            result = json.load(f)
        except :
            return -1,0,0,0,0
            
        owner=result['rows'][0]['owner']
        type=result['rows'][0]['rows'][0]['type']
        attack=result['rows'][0]['rows'][0]['attack']
        defense=result['rows'][0]['rows'][0]['defense']
        hp=result['rows'][0]['rows'][0]['hp']
        damage_per_min=25-(25*defense/(defense+1000))
        alive_sec=int(60*hp/damage_per_min)
        if type == 1:
            a=alive_sec+1000000
        elif type == 2:
            a=alive_sec+2000000
        elif type == 3:
            a=alive_sec+3000000
        alive_sec_re=alive_sec
        current_kill_count=attack*alive_sec/60/200

        owner=result['rows'][0]['owner']
        type=result['rows'][0]['rows'][1]['type']
        attack=result['rows'][0]['rows'][1]['attack']
        defense=result['rows'][0]['rows'][1]['defense']
        hp=result['rows'][0]['rows'][1]['hp']
        damage_per_min=25-(25*defense/(defense+1000))
        alive_sec=int(60*hp/damage_per_min)
        if type == 1:
            b=alive_sec+1000000
        elif type == 2:
            b=alive_sec+2000000
        elif type == 3:
            b=alive_sec+3000000
        if alive_sec > alive_sec_re:
            alive_sec_re = alive_sec
        current_kill_count+=attack*alive_sec/60/200

        owner=result['rows'][0]['owner']
        type=result['rows'][0]['rows'][2]['type']
        attack=result['rows'][0]['rows'][2]['attack']
        defense=result['rows'][0]['rows'][2]['defense']
        hp=result['rows'][0]['rows'][2]['hp']
        damage_per_min=25-(25*defense/(defense+1000))
        alive_sec=int(60*hp/damage_per_min)
        if type == 1:
            c=alive_sec+1000000
        elif type == 2:
            c=alive_sec+2000000
        elif type == 3:
            c=alive_sec+3000000
        if alive_sec > alive_sec_re:
            alive_sec_re = alive_sec
        current_kill_count+=attack*alive_sec/60/200
        floor = (current_kill_count / 10) + 1;
        subprocess.call('rm -f '+filename, shell=True)
        return alive_sec_re,a,b,c,int(floor)

def stepResign():
    print('='*30);
    if (args.name=='null'):
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']
            maxsec,typea,typeb,typec,floor = getAliveSec(name)
            if maxsec == -1:
                continue
                
            last_rebirth = getPlayer(name)
            if last_rebirth == -1:
                continue
            last_rebirth += 1500000000 
            end_time = last_rebirth + maxsec
            timeArray = time.localtime(last_rebirth)
            formatTime= time.strftime("%Y/%m/%d %H:%M:%S", timeArray)

            timeEnd= time.localtime(end_time)
            formatEndTime= time.strftime("%Y/%m/%d %H:%M:%S", timeEnd)

            now = time.time()
            left = 0
            if end_time - now < 0:
                left = 0
            else:
                left = end_time - now 
            m, s = divmod(left, 60)
            h, m = divmod(m, 60)
            print("name:",name);
            print("knta's time:",typea);
            print("kntb's time:",typeb);
            print("kntc's time:",typec);
            print("floor:",floor);
            print("begin time:"+str(formatTime));
            print("end time:"+str(formatEndTime));
            print ("left %02d:%02d:%02d" % (h, m, s))
    else:
            name = args.name
            maxsec,typea,typeb,typec,floor = getAliveSec(name)
            if maxsec == -1:
                return
            last_rebirth = getPlayer(name)
            last_rebirth += 1500000000 
            end_time = last_rebirth + maxsec
            timeArray = time.localtime(last_rebirth)
            formatTime= time.strftime("%Y/%m/%d %H:%M:%S", timeArray)

            timeEnd= time.localtime(end_time)
            formatEndTime= time.strftime("%Y/%m/%d %H:%M:%S", timeEnd)

            now = time.time()
            left = 0
            if end_time - now < 0:
                left = 0
            else:
                left = end_time - now 
            m, s = divmod(left, 60)
            h, m = divmod(m, 60)
            print("name:",name);
            print("knta's time:",typea);
            print("kntb's time:",typeb);
            print("kntc's time:",typec);
            print("floor:",floor);
            print("begin time:"+str(formatTime));
            print("end time:"+str(formatEndTime));
            print ("left %02d:%02d:%02d" % (h, m, s))
        
    print('='*30);

def stepResign1():
    print('='*30);
    if (args.name=='null'):
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']
            maxsec,typea,typeb,typec,floor = getAliveSec(name)
            if maxsec == -1:
                continue
            last_rebirth = getPlayer(name)
            if last_rebirth == -1:
                continue
            last_rebirth += 1500000000
            end_time = last_rebirth + maxsec
            timeArray = time.localtime(last_rebirth)
            formatTime= time.strftime("%Y/%m/%d %H:%M:%S", timeArray)

            timeEnd= time.localtime(end_time)
            formatEndTime= time.strftime("%Y/%m/%d %H:%M:%S", timeEnd)

            now = time.time()
            left = 0
            if end_time - now < 0:
                print('='*30)
                left = 0
                print("name:",name)
                print("begin time:"+str(formatTime))
                print("end time:"+str(formatEndTime))
                print ("left:",left)
                print('='*30)
            else:
                print("name:",name)
    else:
        name = args.name
        maxsec,typea,typeb,typec,floor = getAliveSec(name)
        if maxsec == -1:
            return
        last_rebirth = getPlayer(name)
        last_rebirth += 1500000000
        end_time = last_rebirth + maxsec
        timeArray = time.localtime(last_rebirth)
        formatTime= time.strftime("%Y/%m/%d %H:%M:%S", timeArray)

        timeEnd= time.localtime(end_time)
        formatEndTime= time.strftime("%Y/%m/%d %H:%M:%S", timeEnd)

        now = time.time()
        left = 0
        if end_time - now < 0:
            print('='*30)
            left = 0
            print("name:",name)
            print("begin time:"+str(formatTime))
            print("end time:"+str(formatEndTime))
            print ("left:",left)
            print('='*30)
        else:
            print("name:",name)

def doRebirth():
    if (args.name=='null'):
        print('error!must input name...')
        return

    for i in range(firstProducer, firstProducer + numProducers):
        a = accounts[i]
        name = a['name']
        block = a['block']
        checksum = a['checksum']
        if (name==args.name):
            while True:
                sleep,typea,typeb,typec,floor = getAliveSec(name)
                if sleep == -1:
                    continue
                r=random.randint(5, 60)
                logFile.write('\n'+'='*30+'\n')
                logFile.write('begin at:'+now()+'\n')
                logFile.write("name:"+name+'\n')
                logFile.write("sleep time:"+str(sleep)+'+'+str(r)+'\n')
                logFile.write("a aliveSec:"+str(typea)+'\n')
                logFile.write("b aliveSec:"+str(typeb)+'\n')
                logFile.write("c aliveSec:"+str(typec)+'\n')
                logFile.write("block:"+str(block)+'\n')
                logFile.write("checksum:"+str(checksum)+'\n')
                cmd = args.cleos + 'push action eosknightsio rebirth2 \"[\"' + name +'\",\"'+block+'\",\"'+checksum+'\"]\" -p '+name+'@active' 
                ret=subprocess.getstatusoutput(cmd)
                logFile.write(str(ret)+'\n')
                logFile.write('end at:'+now()+'\n')
                logFile.write('='*30+'\n')
                logFile.flush()
                time.sleep(sleep+r)

def doRebirth1():
    if (args.name!='null'):
        print('error!don not input name...')
        return

    while True:
        logFile.write('doRebirth1 begin at:'+now()+'\n')
        logFile.flush()
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']
            
            maxsec,typea,typeb,typec,floor = getAliveSec(name)
            if maxsec == -1:
                continue
            last_rebirth = getPlayer(name)
            if last_rebirth == -1:
                continue
            last_rebirth += 1500000000 
            end_time = last_rebirth + maxsec
            timeArray = time.localtime(last_rebirth)
            formatTime= time.strftime("%Y/%m/%d %H:%M:%S", timeArray)

            timeEnd= time.localtime(end_time)
            formatEndTime= time.strftime("%Y/%m/%d %H:%M:%S", timeEnd)

            now1 = time.time()
            logFile.write('try:'+name+'\n')
            r=random.randint(1, 10)
            left = 0
            if end_time - now1 < 0:
                logFile.write('\n'+'='*30+'\n')
                logFile.write('now:'+now()+'\n')
                logFile.write("name:"+name+'\n')
                logFile.write("floor:"+str(floor)+'\n')
                logFile.write("a aliveSec:"+str(typea)+'\n')
                logFile.write("b aliveSec:"+str(typeb)+'\n')
                logFile.write("c aliveSec:"+str(typec)+'\n')
                
                block = a['block']
                checksum = a['checksum']                
                cmd = args.cleos + 'push action eosknightsio rebirth2 \"[\"' + name +'\",\"'+block+'\",\"'+checksum+'\"]\" -p '+name+'@active' 
                try:
                    run(cmd)
                except:
                    continue
                    
                logFile.write(str(ret)+'\n')
                logFile.write('now:'+now()+'\n')
                logFile.write('='*30+'\n')        
                logFile.flush()
                doInMoveMat(name)

            time.sleep(r)
            logFile.flush()
        r=random.randint(5, 60)
        logFile.write("sleep:"+str(300+r))
        logFile.write('doRebirth1 end at:'+now()+'\n')
        logFile.flush()
        time.sleep(300+r)
                
def doGetAccount():
    if (args.name=='null'):
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']
            cmd = args.cleos + 'get account ' + name + " |grep available |grep -v KiB |grep -v \"time of unstake request\""
            print(name+":")
            subprocess.call(cmd, shell=True)
    else:
        cmd = args.cleos + 'get account ' + args.name
        print(args.name+":")
        subprocess.call(cmd, shell=True)

def doMaterial():
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    if (args.name=='null'):
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']            
            cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
            subprocess.call(cmd, shell=True)
            time.sleep(1)
            with open(filename) as f:
                result = json.load(f)
                subprocess.call('rm -f '+filename, shell=True)
                account = len(result['rows'][0]['rows'])
                print(name+':'+str(account))
    else:
        name = args.name
        cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
        subprocess.call(cmd, shell=True)
        time.sleep(1)
        with open(filename) as f:
            result = json.load(f)
            subprocess.call('rm -f '+filename, shell=True)
            account = len(result['rows'][0]['rows'])
            print(name+':'+str(account))

def doMaterial1():
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    if (args.name=='null'):
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']            
            cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
            subprocess.call(cmd, shell=True)
            time.sleep(1)
            with open(filename) as f:
                result = json.load(f)
                subprocess.call('rm -f '+filename, shell=True)
                print('*'*10)
                mataccount = 0
                account = len(result['rows'][0]['rows'])
                print(name+':')
                for i in range(0, account):
                    code=result['rows'][0]['rows'][i]['code']
                    saleid=result['rows'][0]['rows'][i]['saleid']
                    if int(code) == int(args.code):
                        mataccount = mataccount + 1
                if mataccount != 0:
                    print(str(args.code)+'\'s count:'+str(mataccount))  
    else:
        name = args.name
        cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
        subprocess.call(cmd, shell=True)
        time.sleep(1)
        with open(filename) as f:
            result = json.load(f)
            subprocess.call('rm -f '+filename, shell=True)
            print('*'*10)
            mataccount = 0
            account = len(result['rows'][0]['rows'])
            print(name+':')
            for i in range(0, account):
                code=result['rows'][0]['rows'][i]['code']
                saleid=result['rows'][0]['rows'][i]['saleid']
                if int(code) == int(args.code):
                    mataccount = mataccount + 1               
            print(str(args.code)+'\'s count:'+str(mataccount))

def doPetex():
    if (args.name=='null'):
        print('error!must input name...')
        return
        
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    name = args.name
    logFile.write(name+'\n')

    while True:
        logFile.write('doPetex begin at:'+now()+'\n')    
        cmd = args.cleos + 'get table eosknightsio eosknightsio petexp -L ' + name + " -U " + name +'a'+ ' > '+filename     
        subprocess.call(cmd, shell=True)
        time.sleep(1) 
        with open(filename) as f:
            result = json.load(f)
            subprocess.call('rm -f '+filename, shell=True)
            account = 0
            mataccount = 0
            accountexp = 0
            accountrows = len(result['rows'])
            listx = []
            if accountrows > 0:
                account = len(result['rows'][0]['rows'])
                accountexp = account
                logFile.write(name+': petexp account:'+str(account)+'\n')                
                for i in range(0, account):
                    code=result['rows'][0]['rows'][i]['code']
                    isback=result['rows'][0]['rows'][i]['isback']
                    end=result['rows'][0]['rows'][i]['end']
                    listx.insert(1,code)
                    dtime = datetime.datetime.now()
                    now1 = int(time.mktime(dtime.timetuple()))
                    
                    #print(now1,end+1500000000,code,isback,end)
                                
                    if(isback == 0 and now1 > end+1500000000):
                        print('return:',code);
                        cmd = args.cleos + 'push action eosknightsio pexpreturn \"[\"' + name +'\",\"'+str(code)+'\"]\" -p '+name+'@active' 
                        subprocess.call(cmd, shell=True)
                        
                #print(listx)
                
            cmd = args.cleos + 'get table eosknightsio eosknightsio pet -L ' + name + " -U " + name +'a'+ ' > '+filename     
            subprocess.call(cmd, shell=True)
            time.sleep(random.randint(1, 3))
            with open(filename) as f:
                result = json.load(f,object_pairs_hook=OrderedDict)
                subprocess.call('rm -f '+filename, shell=True)
                accountrows = len(result['rows'])
                account = 0
                #print(accountrows)
                if accountrows > 0 :
                    account = len(result['rows'][0]['rows'])
                    print('pet account:',str(account))
                    if account > 0 :                        
                        #for i in range(account-1, -1,-1):
                        list=[]
                        for i in range(0, account):
                            knight=result['rows'][0]['rows'][i]['knight']
                            code=result['rows'][0]['rows'][i]['code']
                            if knight == 0:
                                list.insert(1,code)
                                
                        list.sort(reverse=True)
                        #print(list)
                        ret = [ i for i in list if i not in listx ]
                        if len(ret) > 0:
                            print(ret)  
                            end = 8-accountexp
                            print('end:',end,'accountexp',accountexp)
                            if accountexp == 8:
                                cmd = args.cleos + 'push action eosknightsio pexpstart \"[\"' + name +'\",\"'+str(ret[0])+'\"]\" -p '+name+'@active' 
                                subprocess.call(cmd, shell=True)
                                time.sleep(random.randint(2, 10))
                                
                                cmd = args.cleos + 'get table eosknightsio eosknightsio petexp -L ' + name + " -U " + name +'a'+ ' > '+filename     
                                subprocess.call(cmd, shell=True)
                                time.sleep(1) 
                                with open(filename) as f:
                                    result = json.load(f)
                                    subprocess.call('rm -f '+filename, shell=True)
                                    accountrows = len(result['rows'])
                                    
                                    if accountrows > 0:
                                        accountexp = len(result['rows'][0]['rows'])
                                        end = 8-accountexp
                                        for i in range(1, end):
                                            print('start:',ret[i])
                                            cmd = args.cleos + 'push action eosknightsio pexpstart \"[\"' + name +'\",\"'+str(ret[i])+'\"]\" -p '+name+'@active' 
                                            subprocess.call(cmd, shell=True)
                                            time.sleep(random.randint(2, 10)) 
                            else:                                
                                for i in range(0, end):
                                    print('start:',ret[i])
                                    cmd = args.cleos + 'push action eosknightsio pexpstart \"[\"' + name +'\",\"'+str(ret[i])+'\"]\" -p '+name+'@active' 
                                    subprocess.call(cmd, shell=True)
                                    time.sleep(random.randint(2, 10))                                    

        logFile.flush()
        sleeptime = 3600 + random.randint(1, 60)
        logFile.write('doPetexp end at:'+now()+'\n')
        logFile.flush()
        time.sleep(sleeptime)                
            
def doPetexAll():
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    if (args.name!='null'):
        name = args.name 
        logFile.write(name+'\n')
        logFile.flush()
        cmd = args.cleos + 'get table eosknightsio eosknightsio petexp -L ' + name + " -U " + name +'a'+ ' > '+filename     
        runnotlog(cmd)
        time.sleep(1) 
        with open(filename) as f:
            try:
                result = json.load(f)
            except:
                return
            subprocess.call('rm -f '+filename, shell=True)
            account = 0
            mataccount = 0
            accountexp = 0
            accountrows = len(result['rows'])
            listx = []
            if accountrows > 0:
                account = len(result['rows'][0]['rows'])
                accountexp = 0                    
                
                for i in range(0, account):
                    code=result['rows'][0]['rows'][i]['code']
                    isback=result['rows'][0]['rows'][i]['isback']
                    end=result['rows'][0]['rows'][i]['end']
                    listx.insert(1,code)
                    dtime = datetime.datetime.now()
                    now1 = int(time.mktime(dtime.timetuple()))
                    
                    #print(now1,end+1500000000,code,isback,end)
                    if(isback == 0):
                        accountexp = accountexp+1
                    if(isback == 1 and now1 > end+1500000000):
                        try:
                            listx.remove(code)
                        except:
                            print("go on.")
                            
                    if(isback == 0 and now1 > end+1500000000):
                        print('return:',code);
                        cmd = args.cleos + 'push action eosknightsio pexpreturn \"[\"' + name +'\",\"'+str(code)+'\"]\" -p '+name+'@active' 
                        subprocess.call(cmd, shell=True)
                        try:
                            print(listx.pop(1))
                        except:
                            print("go on.")
                        accountexp = accountexp -1   
                        
                                               
                logFile.write(name+': petexp num:'+str(accountexp)+'\n')
                logFile.flush()
                #print(listx)

            cmd = args.cleos + 'get table eosknightsio eosknightsio pet -L ' + name + " -U " + name +'a'+ ' > '+filename     
            subprocess.call(cmd, shell=True)
            time.sleep(random.randint(1, 3))
            with open(filename) as f:
                result = json.load(f,object_pairs_hook=OrderedDict)
                subprocess.call('rm -f '+filename, shell=True)
                accountrows = len(result['rows'])
                account = 0
                #print(accountrows)
                if accountrows > 0 :
                    account = len(result['rows'][0]['rows'])
                    logFile.write(name+': pet num:'+str(account)+'\n')
                    logFile.flush()
                    if account > 0 :                        
                        #for i in range(account-1, -1,-1):
                        list=[]
                        for i in range(0, account):
                            knight=result['rows'][0]['rows'][i]['knight']
                            code=result['rows'][0]['rows'][i]['code']
                            if knight == 0:
                                if args.auto == 'true':
                                    if int(code) > 16:
                                        list.insert(1,code)
                                else: 
                                    if int(code) > 8:
                                        list.insert(1,code)
                                
                        list.sort(reverse=True)
                        ret = [ i for i in list if i not in listx ]
                        print("list:",list,listx)
                        print("ret:",ret,len(ret))
                        if len(ret) > 0:
                            #print(ret)  
                            end = 4-accountexp
                            #print('end:',end,'accountexp',accountexp)
                            if accountexp >= 8:
                                cmd = args.cleos + 'push action eosknightsio pexpstart \"[\"' + name +'\",\"'+str(ret[0])+'\"]\" -p '+name+'@active' 
                                run(cmd)
                                time.sleep(random.randint(2, 10))
                                
                                cmd = args.cleos + 'get table eosknightsio eosknightsio petexp -L ' + name + " -U " + name +'a'+ ' > '+filename     
                                subprocess.call(cmd, shell=True)
                                time.sleep(1) 
                                with open(filename) as f:
                                    result = json.load(f)
                                    subprocess.call('rm -f '+filename, shell=True)
                                    accountrows = len(result['rows'])
                                    accountexp = 0
                                    if accountrows > 0:
                                        account = len(result['rows'][0]['rows'])
                                        
                                        for i in range(0, account):
                                            code=result['rows'][0]['rows'][i]['code']
                                            isback=result['rows'][0]['rows'][i]['isback']
                                            if isback == 0:
                                                accountexp = accountexp + 1
                                                
                                        end = 4-accountexp
                                        if end > 1:                                            
                                            for i in range(1, end):
                                                print('start:',ret[i])
                                                cmd = args.cleos + 'push action eosknightsio pexpstart \"[\"' + name +'\",\"'+str(ret[i])+'\"]\" -p '+name+'@active' 
                                                run(cmd)
                                                time.sleep(random.randint(2, 10)) 
                            else: 
                                print("end:",end,len(ret))
                                if end >= len(ret):
                                    end = len(ret)
                                if end > 0:
                                    for i in range(0, end):
                                        print('start:',ret[i])
                                        cmd = args.cleos + 'push action eosknightsio pexpstart \"[\"' + name +'\",\"'+str(ret[i])+'\"]\" -p '+name+'@active' 
                                        run(cmd)
                                        time.sleep(random.randint(2, 10))  
                                
                        logFile.flush()        
                    logFile.flush()                                  

        logFile.flush()
        return
        
    
    
    while True:
        logFile.write('doPetexAll begin at:'+now()+'\n')
        logFile.flush()
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']   
            logFile.write("try:"+name+'begin.\n')
            logFile.flush()
            cmd = args.cleos + 'get table eosknightsio eosknightsio petexp -L ' + name + " -U " + name +'a'+ ' > '+filename     
            runnotlog(cmd)
            time.sleep(1) 
            with open(filename) as f:
                try:
                    result = json.load(f)
                except:
                    continue
                subprocess.call('rm -f '+filename, shell=True)
                account = 0
                mataccount = 0
                accountexp = 0
                accountrows = len(result['rows'])
                listx = []
                if accountrows > 0:
                    account = len(result['rows'][0]['rows'])
                    accountexp = 0                    
                    
                    for i in range(0, account):
                        code=result['rows'][0]['rows'][i]['code']
                        isback=result['rows'][0]['rows'][i]['isback']
                        end=result['rows'][0]['rows'][i]['end']
                        listx.insert(1,code)
                        dtime = datetime.datetime.now()
                        now1 = int(time.mktime(dtime.timetuple()))
                        
                        #print(now1,end+1500000000,code,isback,end)
                        if(isback == 0):
                            accountexp = accountexp+1
                        if(isback == 1 and now1 > end+1500000000):
                            try:
                                listx.remove(code)
                            except:
                                print("go on.")
                                
                        if(isback == 0 and now1 > end+1500000000):
                            print('return:',code);
                            cmd = args.cleos + 'push action eosknightsio pexpreturn \"[\"' + name +'\",\"'+str(code)+'\"]\" -p '+name+'@active' 
                            subprocess.call(cmd, shell=True)
                            accountexp = accountexp -1   
                            
                                                   
                    #logFile.write(name+': petexp num:'+str(accountexp)+'\n')
                    #logFile.flush()
                    #print(listx)

                cmd = args.cleos + 'get table eosknightsio eosknightsio pet -L ' + name + " -U " + name +'a'+ ' > '+filename     
                subprocess.call(cmd, shell=True)
                time.sleep(random.randint(1, 3))
                with open(filename) as f:
                    try:
                        result = json.load(f,object_pairs_hook=OrderedDict)
                    except:
                        continue
                    subprocess.call('rm -f '+filename, shell=True)
                    accountrows = len(result['rows'])
                    account = 0
                    #print(accountrows)
                    if accountrows > 0 :
                        account = len(result['rows'][0]['rows'])
                        #logFile.write(name+': pet num:'+str(account)+'\n')
                        #logFile.flush()
                        if account > 0 :                        
                            #for i in range(account-1, -1,-1):
                            list=[]
                            for i in range(0, account):
                                knight=result['rows'][0]['rows'][i]['knight']
                                code=result['rows'][0]['rows'][i]['code']
                                if knight == 0:
                                    if args.auto == 'true':
                                        if int(code) > 16:
                                            list.insert(1,code)
                                    else: 
                                        if int(code) > 8:
                                            list.insert(1,code)
                                    
                            list.sort(reverse=True)
                            ret = [ i for i in list if i not in listx ]
                            #print("list:",list,listx)
                            #print("ret:",ret,len(ret))
                            if len(ret) > 0:
                                #print(ret)  
                                end = 4-accountexp
                                #print('end:',end,'accountexp',accountexp)
                                if accountexp >= 8:
                                    cmd = args.cleos + 'push action eosknightsio pexpstart \"[\"' + name +'\",\"'+str(ret[0])+'\"]\" -p '+name+'@active' 
                                    runnotlog(cmd)
                                    time.sleep(random.randint(2, 10))
                                    
                                    cmd = args.cleos + 'get table eosknightsio eosknightsio petexp -L ' + name + " -U " + name +'a'+ ' > '+filename     
                                    subprocess.call(cmd, shell=True)
                                    time.sleep(1) 
                                    with open(filename) as f:
                                        result = json.load(f)
                                        subprocess.call('rm -f '+filename, shell=True)
                                        accountrows = len(result['rows'])
                                        accountexp = 0
                                        if accountrows > 0:
                                            account = len(result['rows'][0]['rows'])
                                            
                                            for i in range(0, account):
                                                code=result['rows'][0]['rows'][i]['code']
                                                isback=result['rows'][0]['rows'][i]['isback']
                                                if isback == 0:
                                                    accountexp = accountexp + 1
                                                    
                                            end = 4-accountexp
                                            if end > 1:                                            
                                                for i in range(1, end):
                                                    print('start:',ret[i])
                                                    cmd = args.cleos + 'push action eosknightsio pexpstart \"[\"' + name +'\",\"'+str(ret[i])+'\"]\" -p '+name+'@active' 
                                                    runnotlog(cmd)
                                                    time.sleep(random.randint(2, 10)) 
                                else: 
                                    print("end:",end,len(ret))
                                    if end >= len(ret):
                                        end = len(ret)
                                    if end > 0:
                                        for i in range(0, end):
                                            print('start:',ret[i])
                                            cmd = args.cleos + 'push action eosknightsio pexpstart \"[\"' + name +'\",\"'+str(ret[i])+'\"]\" -p '+name+'@active' 
                                            runnotlog(cmd)
                                            time.sleep(random.randint(2, 10))  
                                    
                            logFile.flush()        
                        logFile.flush()                                  

            logFile.flush()
        
        sleeptime = 1000 + random.randint(1, 60)
        logFile.write('doPetexAll end at:'+now()+'\n')
        logFile.flush()
        time.sleep(sleeptime)
        
def writefile(name,log):
    name.write(log)
    name.flush()
    
def doGetBalance():
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    if (args.name=='null'):
        writefile(balanceFile, '='*30+'\n')
        writefile(balanceFile, 'begin get balance\n')
        writefile(balanceFile, now()+'\n\n')
        admin = 'eoswangyilin'
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']
            flag = a['flag']
            if flag == '0':
                admin = name
                print("admin:",admin)
                cmd = args.cleos + 'get  currency balance eosio.token ' + name + ' >> '+ args.balancefile
                runnotlog(cmd)
                continue
            
            cmd = args.cleos + 'get  currency balance eosio.token ' + name + ' >> '+filename
            runnotlog(cmd)
            cmd = 'sed -i \''+str(i-1)+'{s/$/& '+ name + '/;}\' ' + filename 
            runnotlog(cmd)
            
        cmd = 'cat ' + filename +' >> ' + args.balancefile 
        runnotlog(cmd)
        writefile(balanceFile, '\n')
        #cmd = 'cat ' + filename +' | sort |awk \'{a+=$1;b+=1;cleos -u http://api-mainnet.starteos.io transfer $3 '+admin+' \"$1 EOS\"}END{print b,a}\'' +' >> ' + args.balancefile 
        cmd = 'cat ' + filename +' | sort |awk \'{a+=$1;b+=1}END{print b,a}\'' +' >> ' + args.balancefile 
        runnotlog(cmd)
          
        writefile(balanceFile, '\nend get balance \n')
        writefile(balanceFile, '='*30+'\n\n')
        subprocess.call('rm -f '+filename, shell=True)
            
    else:
        name = args.name
        cmd = args.cleos + 'get  currency balance eosio.token ' + name 
        runnotlog(cmd)
        
def doClearBalance():
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    if (args.name=='null'):
        
        doGetBalance()
        
        writefile(balanceFile, '*'*30+'\n')
        writefile(balanceFile, 'begin clear balance\n')
        writefile(balanceFile, now()+'\n\n')
        admin = 'eoswangyilin'
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']
            flag = a['flag']
            if flag == '0':                
                admin = name
                print("admin:",admin)
                continue
            if flag == '2':                
                print("not count:",name)
                continue
            
            cmd = args.cleos + 'get  currency balance eosio.token ' + name + ' >> '+filename
            runnotlog(cmd)
            cmd = 'sed -i \''+str(i-1)+'{s/$/& '+ name + '/;}\' ' + filename 
            runnotlog(cmd)
            
        cmd = 'cat ' + filename +' >> ' + args.balancefile 
        runnotlog(cmd)
        writefile(balanceFile, '\n')
        
        cmd = 'cat ' + filename +' | sort |awk \'{a+=$1;b+=1}END{print b,a}\'' +' >> ' + args.balancefile 
        runnotlog(cmd)
        
        cmd = 'cat ' + filename +' | sort |awk \'{a+=$1;b+=1;c=$1-0.1;cmd="cleos -u http://api-mainnet.starteos.io transfer "$3" '+admin+' \\\""c" EOS\\\"";system(cmd);}END{print b,a}\'' +' >> ' + args.balancefile 
        run(cmd)  
        
        writefile(balanceFile, '\nend clear balance \n')
        writefile(balanceFile, '*'*30+'\n\n')
        subprocess.call('rm -f '+filename, shell=True)
        
        doGetBalance()   
    else:
        print("not need name")

def doGetMatNumber(name):
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    cmd = args.cleos + 'get table eosknightsio eosknightsio player -L ' + name + " -U " + name +'a'+ ' > '+filename     
    runnotlog(cmd)
    time.sleep(1)
    with open(filename) as f:
        try:
            result = json.load(f)
        except:
            return -1
            
        subprocess.call('rm -f '+filename, shell=True)
        mat_ivn_up=result['rows'][0]['mat_ivn_up']
        ret=28+mat_ivn_up*4
        return ret
    
def doInMoveMat(abc):
    name = abc
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    movematlist = getmovematlist()
    #print('list:',movematlist)
    cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
    runnotlog(cmd)
    time.sleep(1)
    with open(filename) as f:
        try:
            result = json.load(f)
        except:
            return
        subprocess.call('rm -f '+filename, shell=True)
        account = 0
        mataccount = 0
        accountrows = len(result['rows'])

        if accountrows > 0:
            account = len(result['rows'][0]['rows'])
            rr=doGetMatNumber(name)
            r=rr-3
            if account > r:
                logFile.write('doInMoveMat begin at:'+now()+'\n')
                
                s = ''
                for i in range(0, account):
                    id=result['rows'][0]['rows'][i]['id']
                    code=result['rows'][0]['rows'][i]['code']
                    saleid=result['rows'][0]['rows'][i]['saleid']

                    if saleid != 0:
                        print('in saleing...',code)
                        continue
                    
                    #print("code:",code,id)
                    if str(code) in movematlist:  
                        if i <  account-1:
                            s=s+str(id)+','
                        else:
                            s=s+str(id)
                cmdr = args.cleos + 'push action eosknightsio removemat2 \'[\"' + name +'\",['+s+'],\'30311978\',\'6817300\']\' -p '+name+'@active' 
                run(cmdr)  
                logFile.write('doInMoveMat end at:'+now()+'\n')
                cmd = 'echo \"' + '='*40 +'\" >> ' + "/home/tic/wyl/eosknights/tmp/movemat.log"
                runnotlog(cmd) 
                cmd = 'echo \"' + "account:"+name+ "num:"+str(account) +'\" >> ' + "/home/tic/wyl/eosknights/tmp/movemat.log"
                runnotlog(cmd)
                cmd = 'echo \"' + cmdr +'\" >> ' + "/home/tic/wyl/eosknights/tmp/movemat.log"
                runnotlog(cmd)
                cmd = 'echo \"' + '='*40 +'\" >> ' + "/home/tic/wyl/eosknights/tmp/movemat.log"
                cmd = 'echo \"' + ' '*40 +'\" >> ' + "/home/tic/wyl/eosknights/tmp/movemat.log"
                runnotlog(cmd) 
            else:
                logFile.write('not need doInMoveMat:' +'\n')
            logFile.flush()

def doMoveMat():
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'

    if args.auto == 'true':
        while True:
            logFile.write('doMoveMat begin at:'+now()+'\n')
            logFile.flush()
            for i in range(firstProducer, firstProducer + numProducers):
                a = accounts[i]
                name = a['name']
                
                cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
                subprocess.call(cmd, shell=True)
                time.sleep(1)
                with open(filename) as f:
                    result = json.load(f)
                    subprocess.call('rm -f '+filename, shell=True)
                    account = len(result['rows'][0]['rows'])


                if args.file == "wyl.json":
                    r=33
                else:
                    r=29
                logFile.write("r:"+str(r)+"\n")
                logFile.write("name:"+name+";account:"+str(account)+"\n")
                logFile.flush()
                if account > r:
                    logFile.write('\n'+'='*30+'\n')
                    logFile.write('now:'+now()+'\n')
                    logFile.write("name:"+name+'\n')
                    logFile.write("MoveMat:"+'\n')
   
                    movematlist = getmovematlist()
                    #print('list:',movematlist)
                    cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
                    run(cmd)
                    time.sleep(1)
                    with open(filename) as f:
                        result = json.load(f)
                        subprocess.call('rm -f '+filename, shell=True)
                        account = 0
                        mataccount = 0
                        accountrows = len(result['rows'])

                        if accountrows > 0:
                            account = len(result['rows'][0]['rows'])
                            s = ''
                            for i in range(0, account):
                                id=result['rows'][0]['rows'][i]['id']
                                code=result['rows'][0]['rows'][i]['code']
                                saleid=result['rows'][0]['rows'][i]['saleid']

                                if saleid != 0:
                                    print('in saleing...',code)
                                    continue
                                
                                #print("code:",code,id)
                                if str(code) in movematlist:  
                                    if i <  account-1:
                                        s=s+str(id)+','
                                    else:
                                        s=s+str(id)
                            cmd = args.cleos + 'push action eosknightsio removemat2 \'[\"' + name +'\",['+s+'],\'30311978\',\'6817300\']\' -p '+name+'@active' 
                            ret=subprocess.getstatusoutput(cmd)
                            
                    logFile.write(str(ret)+'\n')
                    logFile.write('now:'+now()+'\n')
                    logFile.write('='*30+'\n')
                    logFile.flush()
                r=random.randint(1, 5)
                time.sleep(r)
            r=random.randint(5, 30)
            logFile.write("sleep:"+str(7200+r))
            logFile.write('doMoveMat end at:'+now()+'\n')
            logFile.flush()
            time.sleep(7200+r)
    else:            
        if (args.name=='null'):
            for i in range(firstProducer, firstProducer + numProducers):
                a = accounts[i]
                name = a['name']
                movematlist = getmovematlist()
                #print('list:',movematlist)
                cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
                run(cmd)
                time.sleep(1)
                with open(filename) as f:
                    result = json.load(f)
                    subprocess.call('rm -f '+filename, shell=True)
                    account = 0
                    mataccount = 0
                    accountrows = len(result['rows'])

                    if accountrows > 0:
                        account = len(result['rows'][0]['rows'])
                        s = ''
                        for i in range(0, account):
                            id=result['rows'][0]['rows'][i]['id']
                            code=result['rows'][0]['rows'][i]['code']
                            saleid=result['rows'][0]['rows'][i]['saleid']

                            if saleid != 0:
                                print('in saleing...',code)
                                continue
                            
                            #print("code:",code,id)
                            if str(code) in movematlist:  
                                if i <  account-1:
                                    s=s+str(id)+','
                                else:
                                    s=s+str(id)
                        cmd = args.cleos + 'push action eosknightsio removemat2 \'[\"' + name +'\",['+s+'],\'30311978\',\'6817300\']\' -p '+name+'@active' 
                        run(cmd)
                    
        else:   
            name = args.name  
            movematlist = getmovematlist()
            #print('list:',movematlist)
            cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
            run(cmd)
            time.sleep(1)
            with open(filename) as f:
                result = json.load(f)
                subprocess.call('rm -f '+filename, shell=True)
                account = 0
                mataccount = 0
                accountrows = len(result['rows'])

                if accountrows > 0:
                    account = len(result['rows'][0]['rows'])
                    s = ''
                    for i in range(0, account):
                        id=result['rows'][0]['rows'][i]['id']
                        code=result['rows'][0]['rows'][i]['code']
                        saleid=result['rows'][0]['rows'][i]['saleid']

                        if saleid != 0:
                            print('in saleing...',code)
                            continue
                        
                        #print("code:",code,id)
                        if str(code) in movematlist:  
                            if i <  account-1:
                                s=s+str(id)+','
                            else:
                                s=s+str(id)
                    cmd = args.cleos + 'push action eosknightsio removemat2 \'[\"' + name +'\",['+s+'],\'30311978\',\'6817300\']\' -p '+name+'@active' 
                    run(cmd)
                
        
def read4file(filename):
    time.sleep(1)
    with open(filename) as f:
        result = json.load(f,object_pairs_hook=OrderedDict)
        subprocess.call('rm -f '+filename, shell=True)
        return result

def getmovematlist():
    movematlist=[]
    with open('/home/tic/wyl/eosknights/move_wat.json') as f:
        a = json.load(f)
        matslen = len(a['mats'])
        mats = a['mats']

        for i in range(0, matslen):
            b = mats[i]
            code = b['code']
            movematlist.insert(1,code)
    return movematlist        
    #print("movematlist:",movematlist)

def getcaft():
    movematlist=[]
    with open('/home/tic/wyl/eosknights/caft.json') as f:
        a = json.load(f)
        matslen = len(a['mats'])
        mats = a['mats']

        for i in range(0, matslen):
            b = mats[i]
            code = b['code']
            movematlist.insert(1,code)
    return movematlist  
    
def doGetItem():
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    
    if (args.name=='null'):
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']
            print(name+':')
            cmd = args.cleos + 'get table eosknightsio eosknightsio item -L ' + name + " -U " + name +'a'+ ' > '+filename     
            run(cmd)
            time.sleep(1)
            with open(filename) as f:
                result = json.load(f)
                subprocess.call('rm -f '+filename, shell=True)
                account = 0
                mataccount = 0
                accountrows = len(result['rows'])

                if accountrows > 0:
                    account = len(result['rows'][0]['rows'])
                    s = ''
                    count_h = 0
                    count_l = 0
                    count_hh = 0
                    for i in range(0, account):
                        id=result['rows'][0]['rows'][i]['id']
                        code=result['rows'][0]['rows'][i]['code']
                        knight=result['rows'][0]['rows'][i]['knight']
                        level=result['rows'][0]['rows'][i]['level']
                        exp=result['rows'][0]['rows'][i]['exp']
                        saleid=result['rows'][0]['rows'][i]['saleid']
                        
                        #print(code,knight,level,exp,saleid)
                        if knight != 0:
                            continue

                        if int(code) == int(args.code) :
                            #print('is code')
                            if int(level) == 2 :
                                count_h=count_h+1+int(exp)
                            elif int(level) == 5 :
                                count_hh=count_hh+1
                            else:
                                count_l=count_l+1+int(exp)
                    if count_hh > 0:
                        print('count_hh:',count_hh)
                    if count_h > 0:
                        print('count_h:',count_h)
                    if count_l > 0:
                        print('count_l:',count_l)
                
    else:   
        name = args.name  
        print(name+':')
        cmd = args.cleos + 'get table eosknightsio eosknightsio item -L ' + name + " -U " + name +'a'+ ' > '+filename     
        run(cmd)
        time.sleep(1)
        with open(filename) as f:
            result = json.load(f)
            subprocess.call('rm -f '+filename, shell=True)
            account = 0
            mataccount = 0
            accountrows = len(result['rows'])

            if accountrows > 0:
                account = len(result['rows'][0]['rows'])
                s = ''
                count_h = 0
                count_hh = 0
                count_l = 0
                for i in range(0, account):
                    id=result['rows'][0]['rows'][i]['id']
                    code=result['rows'][0]['rows'][i]['code']
                    knight=result['rows'][0]['rows'][i]['knight']
                    level=result['rows'][0]['rows'][i]['level']
                    exp=result['rows'][0]['rows'][i]['exp']
                    saleid=result['rows'][0]['rows'][i]['saleid']
                    
                    #print(code,knight,level,exp,saleid)
                    if  knight != 0:
                        continue

                    if int(code) == int(args.code) :
                        #print('is code')
                        if int(level) == 2 :
                            count_h=count_h+1+int(exp)
                        elif int(level) == 5 :
                            count_hh=count_hh+1
                        else:
                            count_l=count_l+1+int(exp)
                            
                if count_hh > 0:
                    print('count_hh:',count_hh)
                if count_h > 0:
                    print('count_h:',count_h)
                if count_l > 0:
                    print('count_l:',count_l)

def doDgfreetk():
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    
    if (args.name=='null'):
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']
            print(name+':')
            for i in range(1, 5):
                cmd = args.cleos + 'push action eosknightsio  dgfreetk \'[\"' + name +'\",'+str(i)+']\' -p '+name+'@active' 
                run(cmd)
    else:
        name = args.name
        print(name+':')
        for i in range(1, 4):
            cmd = args.cleos + 'push action eosknightsio  dgfreetk \'[\"' + name +'\",'+str(i)+']\' -p '+name+'@active' 
            run(cmd)
            
def doSellmat():
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    
    if (args.name=='null'):
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']
            print(name+':')
            r=random.randint(1, 3)
            time.sleep(r)
            cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
            run(cmd)
            time.sleep(1)
            with open(filename) as f:
                result = json.load(f)
                subprocess.call('rm -f '+filename, shell=True)
                account = 0
                mataccount = 0
                accountrows = len(result['rows'])

                if accountrows > 0:
                    account = len(result['rows'][0]['rows'])
                    s = ''
                    count_h = 0
                    count_hh = 0
                    count_l = 0
                    for i in range(0, account):
                        id=result['rows'][0]['rows'][i]['id']
                        code=result['rows'][0]['rows'][i]['code']                   
                        saleid=result['rows'][0]['rows'][i]['saleid']

                        if int(code) == int(args.code) and saleid == 0 :
                            cmd = args.cleos + 'push action eosknightsio sellmat2 \'[\"' + name +'\",'+str(id)+',\"'+str(args.price)+' EOS\"'+',\'30673789\',\'263267029\']\' -p '+name+'@active' 
                            run(cmd)
                            break

                    print('not found code:',args.code)
               
    else:   
        name = args.name  
        cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
        run(cmd)
        time.sleep(1)
        with open(filename) as f:
            result = json.load(f)
            subprocess.call('rm -f '+filename, shell=True)
            account = 0
            mataccount = 0
            accountrows = len(result['rows'])

            if accountrows > 0:
                account = len(result['rows'][0]['rows'])
                s = ''
                count_h = 0
                count_hh = 0
                count_l = 0
                for i in range(0, account):
                    id=result['rows'][0]['rows'][i]['id']
                    code=result['rows'][0]['rows'][i]['code']                   
                    saleid=result['rows'][0]['rows'][i]['saleid']

                    if int(code) == int(args.code) and saleid == 0 :
                        cmd = args.cleos + 'push action eosknightsio sellmat2 \'[\"' + name +'\",'+str(id)+',\"'+str(args.price)+' EOS\"'+',\'30673789\',\'263267029\']\' -p '+name+'@active' 
                        run(cmd)
                        return

                print('not found code:',args.code)

def doCraft():
    filename='/home/tic/wyl/eosknights/tmp/'+str(os.getpid())+'.json'
    
    caftlist = getcaft()
    
    if (args.name=='null'):
        for i in range(firstProducer, firstProducer + numProducers):
            a = accounts[i]
            name = a['name']
            print(name+':')
            
            cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
            runnotlog(cmd)
            time.sleep(1)
            with open(filename) as f:
                mresult = json.load(f)
                subprocess.call('rm -f '+filename, shell=True)
                account = 0
                mataccount = 0
                accountrows = len(mresult['rows'])

                if accountrows > 0:
                    account = len(mresult['rows'][0]['rows'])
                            
                    for i in range(len(caftlist)):      

                        cmd = args.cleos + 'get table eosknightsio eosknightsio ritem -L ' + str(caftlist[i]) + " -U " + str(int(caftlist[i])+1) + ' > '+filename     
                        runnotlog(cmd)
                        
                        time.sleep(1)
                        with open(filename) as f:
                            result = json.load(f)
                            subprocess.call('rm -f '+filename, shell=True)
                            a1 = len(result['rows'])

                            if a1 > 0:
                                itemcode=result['rows'][0]['code']
                                mat1_code=result['rows'][0]['mat1_code'] 
                                mat2_code=result['rows'][0]['mat2_code'] 
                                mat3_code=result['rows'][0]['mat3_code'] 
                                mat4_code=result['rows'][0]['mat4_code'] 
                                mat1_count=result['rows'][0]['mat1_count'] 
                                mat2_count=result['rows'][0]['mat2_count'] 
                                mat3_count=result['rows'][0]['mat3_count'] 
                                mat4_count=result['rows'][0]['mat4_count'] 
                                
                                
                                s=''
                                success=1
                                elist=[]
                                for j in range(0, mat1_count):
                                    m1=0
                                    for k in range(0, account):
                                        id=mresult['rows'][0]['rows'][k]['id']
                                        code=mresult['rows'][0]['rows'][k]['code']                   
                                        saleid=mresult['rows'][0]['rows'][k]['saleid']                                    
                                        
                                        if int(code) == int(mat1_code) and saleid == 0 :  
                                            if id in elist: 
                                                #print("e:",id) 
                                                continue
                                            elist.insert(1,id)
                                            s=s+str(id)+','
                                            m1=1
                                            break
                                    if m1 == 0:
                                        success=0
                                        break
 
                                if success == 0:
                                    continue
                                    
                                for j in range(0, mat2_count):
                                    m2=0
                                    for k in range(0, account):
                                        id=mresult['rows'][0]['rows'][k]['id']
                                        code=mresult['rows'][0]['rows'][k]['code']
                                        saleid=mresult['rows'][0]['rows'][k]['saleid']
                                        
                                        if int(code) == int(mat2_code) and saleid == 0 :
                                            if id in elist: 
                                                #print("e:",id) 
                                                continue
                                            elist.insert(1,id)
                                            s=s+str(id)+','
                                            m2=1
                                            break
                                    if m2 == 0:
                                        success=0
                                        break
                                #print(elist) 
                                #print(s)       
                                if success == 0:
                                    continue
                                    
                                for j in range(0, mat3_count):
                                    m3=0
                                    for k in range(0, account):
                                        id=mresult['rows'][0]['rows'][k]['id']
                                        code=mresult['rows'][0]['rows'][k]['code']
                                        saleid=mresult['rows'][0]['rows'][k]['saleid']
                                        
                                        if int(code) == int(mat3_code) and saleid == 0 :
                                            if id in elist: 
                                                #print("e:",id) 
                                                continue
                                            elist.insert(1,id)
                                            s=s+str(id)+','
                                            m3=1
                                            break
                                    if m3 == 0:
                                        success=0
                                        break
                                #print(elist) 
                                #print(s)       
                                if success == 0:
                                    continue

                                for j in range(0, mat4_count):
                                    m4=0
                                    for k in range(0, account):
                                        id=mresult['rows'][0]['rows'][k]['id']
                                        code=mresult['rows'][0]['rows'][k]['code']
                                        saleid=mresult['rows'][0]['rows'][k]['saleid']
                                        
                                        if int(code) == int(mat4_code) and saleid == 0 :
                                            if id in elist: 
                                                #print("e:",id) 
                                                continue
                                            elist.insert(1,id)
                                            s=s+str(id)+','
                                            m4=1
                                            break
                                    if m4 == 0:
                                        success=0
                                        break
                                #print(elist)   
                                #print(s)     
                                if success == 0:
                                    continue
                                cmd = args.cleos + 'push action eosknightsio craft2 \'[\"' + name +'\",'+str(itemcode)+',['+s[:-1]+'],\'20349922\',\'62328620\']\' -p '+name+'@active'
                                run(cmd)
                                
    else:   
        name = args.name  
        cmd = args.cleos + 'get table eosknightsio eosknightsio material -L ' + name + " -U " + name +'a'+ ' > '+filename     
        runnotlog(cmd)
        time.sleep(1)
        with open(filename) as f:
            mresult = json.load(f)
            subprocess.call('rm -f '+filename, shell=True)
            account = 0
            mataccount = 0
            accountrows = len(mresult['rows'])

            if accountrows > 0:
                account = len(mresult['rows'][0]['rows'])
                        
                for i in range(len(caftlist)):      

                    cmd = args.cleos + 'get table eosknightsio eosknightsio ritem -L ' + str(caftlist[i]) + " -U " + str(int(caftlist[i])+1) + ' > '+filename     
                    runnotlog(cmd)
                    
                    time.sleep(1)
                    with open(filename) as f:
                        result = json.load(f)
                        subprocess.call('rm -f '+filename, shell=True)
                        a1 = len(result['rows'])

                        if a1 > 0:
                            itemcode=result['rows'][0]['code']
                            mat1_code=result['rows'][0]['mat1_code'] 
                            mat2_code=result['rows'][0]['mat2_code'] 
                            mat3_code=result['rows'][0]['mat3_code'] 
                            mat4_code=result['rows'][0]['mat4_code'] 
                            mat1_count=result['rows'][0]['mat1_count'] 
                            mat2_count=result['rows'][0]['mat2_count'] 
                            mat3_count=result['rows'][0]['mat3_count'] 
                            mat4_count=result['rows'][0]['mat4_count'] 
                            
                            
                            s=''
                            success=1
                            elist=[]
                            for j in range(0, mat1_count):
                                m1=0
                                for k in range(0, account):
                                    id=mresult['rows'][0]['rows'][k]['id']
                                    code=mresult['rows'][0]['rows'][k]['code']                   
                                    saleid=mresult['rows'][0]['rows'][k]['saleid']                                    
                                    
                                    if int(code) == int(mat1_code) and saleid == 0 :  
                                        if id in elist: 
                                            print("e:",id) 
                                            continue
                                        elist.insert(1,id)
                                        s=s+str(id)+','
                                        m1=1
                                        break
                                if m1 == 0:
                                    success=0
                                    break
                            print(elist)
                            print(s)  
                            if success == 0:
                                continue
                                
                            for j in range(0, mat2_count):
                                m2=0
                                for k in range(0, account):
                                    id=mresult['rows'][0]['rows'][k]['id']
                                    code=mresult['rows'][0]['rows'][k]['code']
                                    saleid=mresult['rows'][0]['rows'][k]['saleid']
                                    
                                    if int(code) == int(mat2_code) and saleid == 0 :
                                        if id in elist: 
                                            print("e:",id) 
                                            continue
                                        elist.insert(1,id)
                                        s=s+str(id)+','
                                        m2=1
                                        break
                                if m2 == 0:
                                    success=0
                                    break
                            print(elist) 
                            print(s)       
                            if success == 0:
                                continue
                                
                            for j in range(0, mat3_count):
                                m3=0
                                for k in range(0, account):
                                    id=mresult['rows'][0]['rows'][k]['id']
                                    code=mresult['rows'][0]['rows'][k]['code']
                                    saleid=mresult['rows'][0]['rows'][k]['saleid']
                                    
                                    if int(code) == int(mat3_code) and saleid == 0 :
                                        if id in elist: 
                                            print("e:",id) 
                                            continue
                                        elist.insert(1,id)
                                        s=s+str(id)+','
                                        m3=1
                                        break
                                if m3 == 0:
                                    success=0
                                    break
                            print(elist) 
                            print(s)       
                            if success == 0:
                                continue

                            for j in range(0, mat4_count):
                                m4=0
                                for k in range(0, account):
                                    id=mresult['rows'][0]['rows'][k]['id']
                                    code=mresult['rows'][0]['rows'][k]['code']
                                    saleid=mresult['rows'][0]['rows'][k]['saleid']
                                    
                                    if int(code) == int(mat4_code) and saleid == 0 :
                                        if id in elist: 
                                            print("e:",id) 
                                            continue
                                        elist.insert(1,id)
                                        s=s+str(id)+','
                                        m4=1
                                        break
                                if m4 == 0:
                                    success=0
                                    break
                            print(elist)   
                            print(s)     
                            if success == 0:
                                continue
                            cmd = args.cleos + 'push action eosknightsio craft2 \'[\"' + name +'\",'+str(itemcode)+',['+s[:-1]+'],\'20349922\',\'62328620\']\' -p '+name+'@active'
                            run(cmd)
                

parser = argparse.ArgumentParser()

commands = [
    ('b', 'doMaterial',     doMaterial,                 False,    "Resign eosio"),
    ('B', 'doMaterial1',    doMaterial1,                False,    "Resign eosio"),
    ('c', 'account',        doGetAccount,               False,   "Show tail of node's log"),
    ('d', 'dgfreetk',       doDgfreetk,                 False,   "Show tail of node's log"),
    ('e', 'docraft',        doCraft,                    False,   "Show tail of node's log"),
    ('p', 'pet',            doPetex,                    False,   "Show tail of node's log"),
    ('P', 'petALl',         doPetexAll,                 False,   "Show tail of node's log"),    
    ('q', 'resign',         stepResign,                 False,    "Resign eosio"),
    ('Q', 'resign1',        stepResign1,                False,    "Resign eosio"),
    ('m', 'movemat',        doMoveMat,                  False,    "Resign eosio"),    
    ('s', 'sellmat',        doSellmat,                  False,   "Show tail of node's log"),
    ('S', 'checkitem',      doGetItem,                  False,   "Show tail of node's log"),
    ('l', 'getbalance',     doGetBalance,               False,    "Resign eosio"),
    ('L', 'clearbalance',   doClearBalance,             False,    "Resign eosio"),    
    ('r', 'rebirth',        doRebirth,                  False,   "Show tail of node's log"),
    ('R', 'rebirth1',       doRebirth1,                  False,   "Show tail of node's log"),
]

parser.add_argument('--name', metavar='', help="Path to kticd binary", default='null')
parser.add_argument('--file', metavar='', help="Path to kticd binary", default='/home/tic/wyl/eosknights/wyl.json')
parser.add_argument('--price', metavar='', help="Path to kticd binary", default='1')
parser.add_argument('--code', metavar='', help="Path to kticd binary", default='01')
parser.add_argument('--auto', metavar='', help="Path to kticd binary", default='false')
parser.add_argument('--balancefile', metavar='', help="Path to kticd binary", default='/home/tic/wyl/eosknights/balance.log')
parser.add_argument('--cleos', metavar='', help="Cleos command", default='cleos -u http://eosmainnet.medishares.net:80 ')
parser.add_argument('--log-path', metavar='', help="Path to log file", default='/home/tic/wyl/eosknights/nohup.out')
parser.add_argument('--symbol', metavar='', help="The eosio.system symbol", default='EOS')
parser.add_argument('--user-limit', metavar='', help="Max number of users. (0 = no limit)", type=int, default=3000)
parser.add_argument('--max-user-keys', metavar='', help="Maximum user keys to import into wallet", type=int, default=10)
parser.add_argument('-a', '--all', action='store_true', help="Do everything marked with (*)")
parser.add_argument('-H', '--http-port', type=int, default=8000, metavar='', help='HTTP port for cleos')

for (flag, command, function, inAll, help) in commands:
    prefix = ''
    if inAll: prefix += '*'
    if prefix: help = '(' + prefix + ') ' + help
    if flag:
        parser.add_argument('-' + flag, '--' + command, action='store_true', help=help, dest=command)
    else:
        parser.add_argument('--' + command, action='store_true', help=help, dest=command)
        
args = parser.parse_args()

args.cleos += ' ' 

logFile = open(args.log_path, 'a')

balanceFile = open(args.balancefile, 'a')

#logFile.write('\n' +'do.py begin'+ '\n')
print(args.file)
with open(args.file) as f:
    a = json.load(f)
    firstProducer = len(a['users'])
    numProducers = len(a['producers'])
    accounts = a['users'] + a['producers']


    
maxClients = numProducers + 10

haveCommand = False
for (flag, command, function, inAll, help) in commands:
    if getattr(args, command) or inAll and args.all:
        if function:
            haveCommand = True
            function()
if not haveCommand:
    print('bios-boot-tutorial.py: Tell me what to do. -a does almost everything. -h shows options.')
