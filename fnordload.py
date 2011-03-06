import serial
import eSSP

#ser = serial.Serial('/dev/ttyACM0', 9600)
#print ser.portstr

#ser.write('\x7F\x80\x01\x11\x65\x82')
#line = ser.read(6)

command = eSSP.sync()
crc = eSSP.crc(command)

line = eSSP.prepcommand(command, crc)

print str(line);
#print ' '.join([hex(ord(i)) for i in line])
#ser.close()

