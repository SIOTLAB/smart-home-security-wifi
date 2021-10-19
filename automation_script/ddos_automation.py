from __future__ import print_function
from variables import*
from pssh.clients import ParallelSSHClient
from twilio.rest import Client
from paramiko import SSHClient
import multiprocessing
import pandas as pd
import os,time, sys
import subprocess
import paramiko


def main():
	send_message('Note !! Starting Readings !')

	# ssh to sniffer
	cmd = enable_monitor_mode
	ssh_sniffer = connect(sniffer_ip, sniffer_uname, sniffer_passwd)
	try:
		execute(ssh_sniffer,cmd)
		print ('ssh to sniffer is successful and monitor mode is enabled')
	except Exception as e:
		raise Exception(e)

	# creat object to ssh into attacker, sniffer and AP simultaneously
	try:
		parallelssh = ParallelSSHClient(hosts_ddos, host_config = hosts_ddos_credentials) 
		print ('ssh to sniffer, empiot, AP is successful')   
	except Exception as e:
		raise Exception(e)



	#### start readings
	for payload in payloads:
		for hping_interval, attack_rate in zip(hping_intervals, attack_rates):
			start_readings_ddos(hping_interval,attack_rate,attack_id,attack_name, \
				reading_id,run_time,intrim_wait,device_ip,payload)

	send_message('Success! All Readings Done !!')


if __name__ == '__main__':
    main()

