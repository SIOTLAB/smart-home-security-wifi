import sys
import brainstem 
from brainstem.result import Result


def control(id,state):
	#for reference check usbhub3p_example.py
	stem1 = brainstem.stem.USBHub3p()                                       
	result = stem1.discoverAndConnect(brainstem.link.Spec.USB)
	if result == (Result.NO_ERROR):
	    result = stem1.system.getSerialNumber()
	    #print ("Connected to USBStem with serial number: 0x%08X"%(result.value),result.value)    
	else:
		print(result)
		print ('Could not find a module.\n')
		raise Exception('Exception In Connecting to the USBStem.')
		sys.exit(1)
	if state ==  'on':
		stem1.usb.setPowerEnable(id)
	else:
		stem1.usb.setPowerDisable(id)

def help():
	print('Valid Command Format\n')
	print('python ./scripts/usb_control.py switch:<id> <on/off>')
	print('Example Commands\n')
	print('''
	python ./scripts/usb_control.py switch:0 on
	python ./scripts/usb_control.py switch:0 off
	''')
	sys.exit(1)

if __name__ == '__main__':
	args = sys.argv

	if len(args) != 3: # 0th argument is the file name
		print('Please enter valid arguments')
		help()
	if not args[1].startswith('switch:'):
		print('Invalid Command')
		help()
	
	id = int(args[1].split('switch:')[1])
	if id < 0 or id > 7:
		print('Invalid Switch Id!')
		print('Valid Switch Ids Range from 0,1,...,7')
		help()
	state = args[2]
	if state not in ['on','off']:
		print('Invalid State',state)
		help()
	
	control(id,state)