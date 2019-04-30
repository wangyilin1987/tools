set -o vi

alias lt='ls -lrt'
date=`date +%Y%m%d`
alias c='clear'

alias l='ls -ltrF'
alias lt='ls -ltr'
alias h='history'
alias psl='ps -eo pid,lstart,etime,cmd'

#alias cleose='cleos -u https://node1.eoscannon.io '
#alias cleose='cleos -u https://mainnet.eoscannon.io '
#alias cleose='cleos -u http://api-mainnet.starteos.io '
#alias cleose='cleos -u http://peer1.eoshuobipool.com:8181 '
#http://eos.greymass.com support cleos get actions
#http://eu.eosdac.io cleos get actions
alias cleose='cleos -u http://eosmainnet.medishares.net:80 '
alias cleosj='cleos -u http://jungle.cryptolions.io:18888 '
alias cleost='cleos -u http://47.96.237.226:8888 '

#bos链节点
alias cleosb='cleos -u https://api-bos.starteos.io/ '
export PATH="/home/wangyilin/Downloads/soft/nvm/versions/node/v10.15.1/bin:$PATH"
export PATH="/home/wangyilin/opt/eosio/bin:$PATH"


export PS1='[wangyilin@$PWD]'

. ~/wyl/tools/wall.sh


