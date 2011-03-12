from struct import *
import logging

LOG_FILENAME = 'logs/eSSP.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

ssp_sequence = '0x80'
ssp_address = 0

# Start Of Definition Of SSP_CMD_* Commands

def reset():
	command = [getseq(), '0x1', '0x1']
	return command

def set_inhibits(lowchannels, highchannels):
	command = [getseq(), '0x3', '0x2', lowchannels, highchannels]
	return command

def bulb_on():
	command = [getseq(), '0x1', '0x3']
	return command

def bulb_off():
	command = [getseq(), '0x1', '0x4']
	return command

def setup_request():
	command = [getseq(), '0x1', '0x5']
	return command

def host_protocol(host_protocol):
	command = [getseq(), '0x2', '0x6', host_protocol]
	return command

def poll():
	command = [getseq(), '0x1', '0x7']
	return command

def reject_note():
	command = [getseq(), '0x1', '0x8']
	return command

def disable():
	command = [getseq(), '0x1', '0x9']
	return command

def enable():
	command = [getseq(), '0x1', '0xA']
	return command

# SSP_CMD_PROGRAM 0xB not implented

def serial_number():
	command = [getseq(), '0x1', '0xC']
	return command

def unit_data():
	command = [getseq(), '0x1', '0xD']
	return command

def channel_values():
	command = [getseq(), '0x1', '0xE']
	return command

def channel_security():
	command = [getseq(), '0x1', '0xF']
	return command

def channel_reteach():
	command = [getseq(), '0x1', '0xG']
	return command

def sync():
	global ssp_sequence
	
	#set ssp_sequence to 0x00, so next will be 0x80 by default
	ssp_sequence = '0x00'
	
	command = [getseq(), '0x1', '0x11']
	return command

# SSP_CMD_DISPENSE 0x12 not implented

# SSP_CMD_PROGRAM_STATUS 0x16 not implented

def last_reject():
	command = [getseq(), '0x1', '0x17']
	return command

def hold():
	command = [getseq(), '0x1', '0x18']
	return command

# SPP_CMD_MANUFACTURER 0x30 not implented - collides with SSP_CMD_EXPANSION ?!

# SSP_CMD_EXPANSION 0x30 not implented - collides with SSP_CMD_MANUFACTURER ?!

def enable_higher_protocol():
	command = [getseq(), '0x1', '0x19']
	return command
	
# End Of Definition Of SSP_CMD_* Commands


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
