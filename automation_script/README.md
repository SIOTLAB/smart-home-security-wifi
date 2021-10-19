## eddos_automation.py and ddos_automation.py are automated Python scripts for an efficient E-DDoS attack and DDoS attack data collection, respectively, against various WiFi-based IoT devices. The script runs on the command and control center, which manages the various components of the testbed. 
The testbed contains Google Mini Home, Amazon Echo Dot, Nest Indoor Camera, and Ring Stick Up Camera as victim IoT devices. Four Linux machines are used as:
an attacker to send malicious packets to the victim devices,
an AP,
a sniffer to capture WiFi traffic, and
a command and control center to coordinate the testbed components.
A programmable power switch is used to turn on/off the connected devices automatically. The EMPIOT board is used to measure the power consumption of the victim device in real-time. 
![image](https://user-images.githubusercontent.com/33651055/137239411-4280191d-9a28-42f6-869f-b5c1d75722d8.png)

We use the following Python libraries and API for its implementation -- Pandas, Paramiko parallel ssh python library, and Twilio Python API. Twilio Python API is used to monitor the script's operation, such as if an error occurs, a message is sent to us, and the Paramiko library is used to SSH into various hardware devices in the testbed. 

It has the following submodules:
usb_control.py: This module helps to turn on/off the USB plug of the programmable power switch. 
variables.py: This module contains the variables used in the script.
helper.py: This module contains different functions that are used in the script.
monitor.sh: the shell script enables the monitor mode on the sniffer. 

## To run the script, please set up the following environment variables:
sniffer_uname, empiot_uname, attacker_uname, ap_uname
sniffer_passwd, attacker_passwd, empiot_passwd, ap_uname
 sniffer_ip, empiot_ip, attacker_ip, ap_ip
device_ip, device_name.
The script launches the following attacks against IoT devices -- TCP, UDP, and ICMP with two payload settings:  0 B and 1400 B.
For more information and better visualization, please refer to our work:
http://behnam.dezfouli.com/publication/IOTJ-WiFi-SmartHome-2020.pdf