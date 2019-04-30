#翻墙软件启动脚本
sudo pkill sslocal
sudo nohup sslocal -c /etc/shadowsocks-libev/shadowlocal.json &
sudo service polipo stop
sudo service polipo start

export http_proxy="http://127.0.0.1:8787"
export https_proxy="http://127.0.0.1:8787"
