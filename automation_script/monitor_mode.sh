sudo rfkill unblock wifi
sudo ifconfig wlp3s0 up
# sudo iwconfig wlp3s0 channel 40
# sudo iwconfig wlp3s0 freq 5200Mhz
sudo iwconfig wlp3s0 channel 1
sudo iwconfig wlp3s0 freq 2412Mhz 
sudo ifconfig wlp3s0 down
sudo iwconfig wlp3s0 mode monitor
sudo ifconfig wlp3s0 up
# sudo iwconfig wlp3s0 channel 40
# sudo iwconfig wlp3s0 freq 5200Mhz
sudo iwconfig wlp3s0 channel 1
sudo iwconfig wlp3s0 freq 2412Mhz
sudo iwconfig wlp3s0
sudo iwconfig wlp3s0 channel 1
# sudo iwconfig wlp3s0 channel 40
# sudo iwconfig wlp3s0 freq 5200Mhz

