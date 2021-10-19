from __future__ import print_function
from variables import*
from helper import*
from pssh.clients import ParallelSSHClient
from paramiko import SSHClient
import pandas as pd
import os,time, sys
import paramiko
from twilio.rest import Client


def main():
	# send message to phone
	send_message('Note !! starting readings !')

	# ssh to sniffer
	cmd = enable_monitor_mode
	ssh_sniffer = connect(sniffer_ip, sniffer_uname, sniffer_passwd)

	# enable monitor mode on sniffer
	try:
		execute(ssh_sniffer,cmd)
		print ('ssh to sniffer is successful and monitor mode is enabled')
	except Exception as e:
		raise Exception(e)


	# creat object to ssh into attacker, sniffer and empiot simultaneously
	try:
		parallelssh = ParallelSSHClient(hosts_eddos, host_config = hosts_eddos_credentials) 
		print ('ssh to attacker, sniffer and empiot is successful')   
	except Exception as e:
		raise Exception(e)


	#### start readings
	for payload in payloads:
		for hping_interval, attack_rate in zip(hping_intervals, attack_rates):
			start_readings(hping_interval,attack_rate,attack_id,attack_name, reading_id,run_time, \
				intrim_wait,device_ip,payload)

	send_message('Success! All Readings Done !!')

if __name__ == '__main__':
    main()

