# This code converts pcap file to csv file

import os
from variables import *

for device in devices:
for attack_type in attack_types:
    for attack_th in attack_throughputs:
        for reading_id in range (0,fileCount):
            out_name= device+attack_type+str(attack_th)+'out'+str(reading_id)
            
            file_path_pcap = 'file_path/%s'%(device)
            file_path_csv = 'file_path/%s/csv'%(device)
            cmd = 'tshark -r %s/%s.pcap -T fields -e _ws.col.Retry -E header=y -E separator=r=,>%s/%s.csv'\
                    %(file_path_pcap,out_name,file_path_csv,out_name)
            try:
                os.system(cmd)
            except:   
                print ('error')
