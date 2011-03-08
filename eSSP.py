from struct import *
import logging

LOG_FILENAME = 'logs/eSSP.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

def sync():
	command = ['0x80', '0x01', '0x11']
	return command

def crc(command):
	length = len(command)
	seed = int('0xFFFF', 16)
	poly = int('0x8005', 16)
	crc = seed

	logging.debug( " 1 || " + hex(crc) )

	for i in range(0, length):
		logging.debug( " 2 || " + str(i) )
		crc ^= ( int(command[i], 16) << 8 )
		logging.debug( " 3 || " + command[i] )
		logging.debug( " 4 || " + hex(crc) )

		for j in range(0, 8):
			logging.debug( " 5 || " + str(j) )

			if ( crc & int('0x8000', 16) ):
				logging.debug( " 6 || " + hex(crc) )
				crc = ( (crc << 1) & int('0xffff', 16) ) ^ poly
				logging.debug( " 7 || " + hex(crc) )
			else:
				crc <<= 1;
				logging.debug( " 8 || " + hex(crc) )
	
	crc = [hex( (crc & 0xFF) ), hex( ((crc >> 8) & 0xFF) )]

	return crc
	
def prepcommand(command, crc):
	prepedstring = '7F'

	for i in range(0, len(command)):
		prepedstring += command[i][2:4]
	
	prepedstring += crc[0][2:4] + crc[1][2:4]
	
	prepedstring = prepedstring.decode('hex')
	
	return prepedstring
