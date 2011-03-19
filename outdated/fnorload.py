import serial
import eSSP

ser = serial.Serial('/dev/ttyACM0', 9600)
print ser.portstr

command = eSSP.sync()
crc = eSSP.crc(command)
line = eSSP.prepcommand(command, crc)
print ' '.join([hex(ord(i)) for i in line])

ser.write(line);
line = ser.read(6)
print ' '.join([hex(ord(i)) for i in line])

# Next

command = eSSP.serial_number()
crc = eSSP.crc(command)
line = eSSP.prepcommand(command, crc)
print ' '.join([hex(ord(i)) for i in line])
ser.write(line);

response = ser.read(3)
response += ser.read(ord(response[2]) + 2)
print ' '.join([hex(ord(i)) for i in response])
print eSSP.calc_serial( response )

ser.close()
