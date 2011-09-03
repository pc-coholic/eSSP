import eSSP
import time

k = eSSP.eSSP('/dev/ttyACM0')
#print k.sync()
#print k.serial_number()
#print k.enable()
#print k.bulb_on()
#print k.bulb_off()
#print k.enable_higher_protocol()
#print k.poll()
#print k.set_inhibits('0xFF', '0xFF')
#print k.set_inhibits(k.easy_inhibit([1, 0, 1]), '0x00')
#print k.unit_data()
#print k.setup_request();
#k.disable();
#k.reset();
#print k.channel_security();
#print k.channel_values();
#print k.channel_reteach();

print k.sync()
print k.enable_higher_protocol()
print k.set_inhibits(k.easy_inhibit([1, 0, 1]), '0x00')
print k.enable()
var = 1
i = 0
while var == 1:
	poll = k.poll()
	print "Poll"
	
	if len(poll) > 1:
		if len(poll[1]) == 2:
			if poll[1][0] == '0xef':
				if poll[1][1] == 1 or poll[1][1] == 3:
					while i < 10:
						k.hold()
						print "Hold " + str(i)
						time.sleep(0.5)
						i += 1
			if poll[1][0] == '0xee':
				print "Credit on Channel " + str(poll[1][1])
				i = 0
				
	time.sleep(0.5)
