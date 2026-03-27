import os
os.system("ip a > /data/data/com.termux/files/usr/tmp/ipdump_$(date +%s).txt")
