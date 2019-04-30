#!/bin/bash
while :; do
   time=`ps -ef |grep "cleos" |grep "eosknightsio" | awk '{print $2}'|wc -l`
   echo "begin clear have:$time"
   if [ $time -ne 0 ];then
        echo "`ps -ef |grep "cleos" |grep "eosknightsio"`"
        for i in `ps -ef |grep "cleos" |grep "eosknightsio" | awk '{print $2}'`;do
            sleep 100
            echo "kill $i"
            kill  $i
        done
   fi
   echo "end clear have:$time"
   sleep 900
done
