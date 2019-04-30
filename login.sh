#!/usr/bin/expect

# 远程连接脚本.eg:sss 47.96.237.226
set ip [lindex $argv 0]
set timeout 30
spawn ssh -l tic  $ip
send "su - tic \r"
expect "Password:"
send "Aasafe123\r"
interact
