import eSSPc
import time

k = eSSPc.eSSPc('/dev/ttyACM0')
print k.sync()
print k.serial_number()
#print k.enable()
#print k.enable_higher_protocol()
#print k.set_inhibits('0xFF', '0xFF')
#print k.bulb_off()
#for i in range(0, 10):
#	print k.poll()
#	time.sleep(0.5)
#print k.bulb_on()

print k.unit_data()
