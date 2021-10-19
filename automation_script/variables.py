
# variables used 
attack_duration   = 180 # seconds
intrim_wait       = 10 # seconds to wait so that empiot and device restarts
run_time          = 45 # wait until sniffer sniffs the data when IoT device is starting
convert_csv_time  = 10 #csv to pcap conversion time (10)
attack_rates	  = os.environ.get('attack_rates')  # packet per second
hping_intervals   = os.environ.get('hping_intervals')
attack_id	  = 0  # icmp:0, tcp:1, udp:2
reading_id        = 0
m 		  = 0  # to make sure all readings are taken after port not found
low 		  = "low"
high 		  = "high"
payloads	  = [low, high]
enable_monitor_mode = './monitor_mode.sh'
ap_event_log        = "./give_timestamp.sh |& tee -a ddos_start_time.csv"
TCP 		    = "tcp"
UDP 		    = "udp"
ICMP 		    = "icmp"
attack_name	    = [ICMP,TCP,UDP]
number_of_attacks   = 30 # (10 readings each for, ICMP, TCP and UDP)
local_fpath	   = os.environ.get('file_path') # csv file is stored on mac also
csv_file_name	   = 'csv_file_name.csv' # file to save csv file to find port number
portnumber_file	   = 'portnumber_file.csv' # save attacked port number
device_name	   = os.environ.get('victim_device_name')
device_ip	   = os.environ.get('device_ip')
attacker_ip	   = os.environ.get('attacker_uname')
sniffer_uname	   = os.environ.get('sniffer_uname')
empiot_uname 	   = os.environ.get('empiot_uname')
ap_uname	   = os.environ.get('ap_uname')
sniffer_passwd	   = os.environ.get('sniffer_passwd')
empiot_passwd	   = os.environ.get('empiot_passwd')
attacker_passwd	   = os.environ.get('attacker_passwd')
ap_passwd 	   = os.environ.get('ap_passwd')
empiot_ip	   = os.environ.get('empiot_ip')
sniffer_ip         = os.environ.get('sniffer_ip')
attacker_ip	   = os.environ.get('attacker_ip')
hosts_ddos 	   = [sniffer_ip, empiot_ip, attacker_ip]
hosts_ddos_credentials = {sniffer_ip : {'user': sniffer_uname, 'password': sniffer_passwd},
			   		 empiot_ip :  {'user': empiot_uname,  'password': empiot_passwd},
			   		 attacker_ip :  {'user': attacker_uname,  'password': attacker_passwd}}
host_eddos 	   = [sniffer_ip,ap_ip, attacker_ip]
hosts_eddos_credentials = {sniffer_ip : {'user': sniffer_uname, 'password': sniffer_passwd},
			   ap_ip : {'user': ap_uname, 'password': ap_passwd},
			   attacker_ip :  {'user': attacker_uname,  'password': attacker_passwd}} 
