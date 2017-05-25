#!/bin/bash
url=$1
times=$2

#verify Speedtest installation
ls -ltr /usr/bin/speedtest-cli
#echo $?
if [ $? != 0 ]; then
   #Create Directory
   cd
   mkdir speedtest-script
   cd speedtest-script
   #Download speedtest_cli directory
   wget https://github.com/sivel/speedtest-cli/archive/master.zip
   unzip master.zip
   cd speedtest-cli-master/
   chmod 755 speedtest_cli.py
   sudo mv speedtest.py /usr/bin/speedtest-cli
fi

echo $times
i=0

while [ $times != 0 ]
do

        #Test Speedtest
        speedtest-cli --mini http://$url/mini/index.html >> testfile.txt

        grep 'load:' testfile.txt
        (( times-- ))
        echo $times
done
