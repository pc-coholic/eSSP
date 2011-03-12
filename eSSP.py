from struct import *
import logging

LOG_FILENAME = 'logs/eSSP.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

ssp_sequence = '0x80'
ssp_address = 0

def sync():
	global ssp_sequence
	
	#set ssp_sequence to 0x00, so next will be 0x80 by default
	ssp_sequence = '0x00'
	
	command = [getseq(), '0x01', '0x11']
	return command
	
def reset():
	command = [getseq(), '0x01', '0x1']
	return command

def getseq():
	global ssp_sequence
	
	# toggle SEQ between 0x80 and 0x00
	if ( ssp_sequence == '0x80' ):
		ssp_sequence = '0x00'
	else :
		ssp_sequence = '0x80'
		
	returnseq = hex( ssp_address | int(ssp_sequence, 16) )
	
	return returnseq
	
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

	command = command + crc

	for i in range(0, len(command)):
		if ( len(command[i]) % 2 == 1):
			prepedstring += '0'
		
		prepedstring += command[i][2:]
	
	prepedstring = prepedstring.decode('hex')
	
	return prepedstring
