#!usr/bin/python
import paramiko
import time
from datetime import datetime

def ip_handling(i):
	global j, k

	if (i%254 == 0):
		j=j+1
		k=1
	ip_server="10.1."+str(j)+"."+str(k)
	#ip_server="10.1."+str(i)+".0"
	ip_client="10.2."+str(j)+"."+str(k)
	print ip_server, ip_client

	return ip_server, ip_client
	

def create_gre_tunnel_server(ip, ip_server, ip_client ):
	success=0
	global j, k

	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip, username='root', password='123456')
	
	tunnel = "gre"+str(i)
	#Add tunnel 
	cmd = "ip tunnel add " + tunnel + " mode gre remote 60.1.1.2 local 60.1.1.1 key " + str(i)
	stdin, stdout, stderr = ssh.exec_command(cmd)
	#Handling IP

	
	local_net=str(ip_server)+"/32"
	tun_ip=str(ip_server)
	dest_ip=str(ip_client)+"/32"
	#Add IP to tunnel interface
	cmd = "ip addr add " + local_net +" dev " +tunnel
	#print cmd
	stdin, stdout, stderr = ssh.exec_command(cmd)
	#Bring up tunnel interface
	cmd = "ip link set " + tunnel + " up"
	stdin, stdout, stderr = ssh.exec_command(cmd)
	#Set the tunnel MTU to 1450
	cmd = "ip link set " + tunnel + " mtu 1450"
	stdin, stdout, stderr = ssh.exec_command(cmd)
	# Add the static route to other end
	cmd = "ip route add " + dest_ip + " via " + tun_ip + " dev " + tunnel
	#print cmd
	stdin, stdout, stderr = ssh.exec_command(cmd)

	#Verify tunnel creation
	cmd = "ifconfig "+tunnel
	stdin, stdout, stderr = ssh.exec_command("ifconfig")
	data = stdout.readlines()
	#print "Data: ", data

	for line in data:
		#print "Line: ", line
		words=line.split()
		#print "Words: ", words
		if not words:
			#dummy command
			tunnel = tunnel
		else:
			if (words[0] == tunnel):
				success = 1
				print "Server Tunnel Created: ", tunnel
	return success

				
def create_gre_tunnel_client(ip, ip_server, ip_client):
	success = 0

	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip, username='root', password='123456')
	
	tunnel = "gre"+str(i)
	#Add tunnel 
	cmd = "ip tunnel add " + tunnel + " mode gre remote 60.1.1.1 local 60.1.1.2 key " + str(i)
	stdin, stdout, stderr = ssh.exec_command(cmd)
	#Add IP to tunnel interface

	local_net=str(ip_client)+"/32"
	tun_ip=str(ip_client)
	dest_ip=str(ip_server)+"/32"
	cmd = "ip addr add " + local_net +" dev " +tunnel
	#print cmd
	stdin, stdout, stderr = ssh.exec_command(cmd)
	#Bring up tunnel interface
	cmd = "ip link set " + tunnel + " up"
	stdin, stdout, stderr = ssh.exec_command(cmd)
	#Set the tunnel MTU to 1450
	cmd = "ip link set " + tunnel + " mtu 1450"
	stdin, stdout, stderr = ssh.exec_command(cmd)
	# Add the static route to other end
	cmd = "ip route add " + dest_ip + " via " + tun_ip + " dev " + tunnel
	#print cmd
	stdin, stdout, stderr = ssh.exec_command(cmd)

	#Verify tunnel creation
	cmd = "ifconfig "+tunnel
	stdin, stdout, stderr = ssh.exec_command("ifconfig")
	data = stdout.readlines()

	for line in data:
		words=line.split()
		if not words:
			#dummy command
			tunnel = tunnel
		else:
			if (words[0] == tunnel):
				success = 1
				print "Client Tunnel Created: ", tunnel
	return success

j=10
k=1

starttime_server = datetime.now()
starttime_client = datetime.now()
print "Current Time: ", datetime.now()

for i in range (1,2):
	ip_server, ip_client= ip_handling(i)
	time_server = datetime.now()
	print "############ Server ###############"
	#print "Before Tun- ", i, time_server
	server = create_gre_tunnel_server("10.9.91.51", ip_server, ip_client)
	if (server == 1):
	#	print "Current Time: ", datetime.now()
		print "Time take for Tunnel-", i, datetime.now()-time_server
		print "Server Tunnel-%d Pass: " %i
	time_client = datetime.now()
	print "############ Client ###############"
	#print "Before Tun- ", i, time_client
	client = create_gre_tunnel_client("10.9.91.52", ip_server, ip_client)
	if (client == 1):
	#	print "Current Time: ", datetime.now()
		print "Time take for Tunnel-", i, datetime.now()-time_client
		print "Client Tunnel-%d Pass: " %i
	#print "Client Tunnel: ", client
	k=k+1

print "#################################"
print "Current Time: ", datetime.now()

