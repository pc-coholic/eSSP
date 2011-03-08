import serial
import eSSP

ser = serial.Serial('/dev/ttyACM0', 9600)
print ser.portstr

command = eSSP.sync()
crc = eSSP.crc(command)

line = eSSP.prepcommand(command, crc)
print line
print ' '.join([hex(ord(i)) for i in line])

ser.write(line);
line = ser.read(6)

print ' '.join([hex(ord(i)) for i in line])
ser.close()

