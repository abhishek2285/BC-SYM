#!usr/bin/python
import paramiko
import re
import time
import datetime
import os
from threading import Thread

#############
#In this Script we test Alteon LB when the servers
#are added onto multiple Service groups with 1 vip per server group
#Change cips & vips to change the client IP's and Virtual IP's
#############

###Run wget from client

def wget(dip, sip):
	print "#######################"
	timestr = datetime.datetime.utcnow().strftime("%H:%M:%S.%f")
	cmd = "wget "+dip+" "+"--bind-address="+sip+" -O /root/test_LB/"+sip+"_"+dip+"txt"+timestr
	print cmd
	stdin, stdout, stderr = ssh.exec_command(cmd)
	cmd = "cat /root/test_LB/"+sip+"_"+dip+"txt"+timestr
	stdin, stdout, stderr = ssh.exec_command(cmd)
	data = stdout.readlines()
	for line in data:
		#print line
		regex=r'Server-(\d)'
		serverMatch = re.search(regex, line, flags=0)
		#print serverMatch
		if serverMatch:
			#print line
			print sip +" going to " + dip + " hit the " + serverMatch.group(0)
			print serverMatch.group(1)
			return serverMatch.group(1)
	print "#######################"

	return


ip = "10.9.91.24"
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username='root', password='l10sm3')
cmd = "cd test_LB; ls -ltr"
#cmd = "ls -ltr"
stdin, stdout, stderr = ssh.exec_command(cmd)
print "#######################"
data = stdout.readlines()



vips=["192.168.1.100", "192.168.1.101", "192.168.1.102"]
cips=["192.168.1.2", "192.168.1.3", "192.168.1.4"]

threads = []
###Test-1: Single Client to multiple VIP's
# print "Test-1"
# for i in range(0,5):

# 	for i in vips:
# 		print "\nTest-1: Run-", i
# 		wget(i, cips[0])
	# 	t = Thread(target=wget, args=(i, cip[0],))
	# 	t.start()
	# 	threads.append(t)
	# 	#print threads

	# for t in threads:
	# 	t.join()



time.sleep(1)


	# vip1= wget(vips[0], cip[0])
	# vip2= wget(vips[1], cip[0])
	# vip3= wget(vips[2], cip[0])

###Test-2: Multiple Clients to Single VIP
# print "\n\nTest-2"

# for i in range(0,5):

# 	for i in cips:
# 		print "\nTest-1: Run-", i
# 		wget(vips[0], i)

# for i in range(0,5):
# 	print "\nTest-2: Run-", i

# 	cip1= wget(vips[0], cip[0])
# 	cip2= wget(vips[0], cip[1])
# 	cip3= wget(vips[0], cip[2])

server1=server2=server3=fail=0
print "\n\nTest-3"

for a in range(0,5):

	for i in cips:
		for j in vips:
			sgserver = wget(j,i)
			print sgserver
			if (sgserver) == "3":
				server3 = server3+1
			elif (sgserver) == "2":
				server2 = server2+1
			elif (sgserver) =="1":
				server1 = server1+1
			else:
				fail = fail+1


print "server3= ", server3
print "server2= ", server2
print "server1= ", server1
print "Fail=", fail

#print data