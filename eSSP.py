import serial
import logging

LOG_FILENAME = 'logs/eSSP.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

class eSSP(object):
	def __init__(self, serialport = '/dev/ttyUSB0', eSSPId = 0):
		self.__ser = serial.Serial(serialport, 9600)
		self.__eSSPId = eSSPId
		self.__sequence = '0x80'
		
# Start Of Definition Of SSP_CMD_* Commands
	def reset(self):
		result = self.send([self.getseq(), '0x1', '0x1'])
		return result

	def set_inhibits(self, lowchannels, highchannels):
		result = self.send([self.getseq(), '0x3', '0x2', lowchannels, highchannels])
		return result

	def bulb_on(self):
		result = self.send([self.getseq(), '0x1', '0x3'])
		return result

	def bulb_off(self):
		result = self.send([self.getseq(), '0x1', '0x4'])
		return result

	def setup_request(self):
		result = self.send([self.getseq(), '0x1', '0x5'])
		return result

	def host_protocol(self, host_protocol):
		result = self.send([self.getseq(), '0x2', '0x6', host_protocol])
		return result

	def poll(self):
		result = self.send([self.getseq(), '0x1', '0x7'])
		return result

	def reject_note(self):
		result = self.send([self.getseq(), '0x1', '0x8'])
		return result

	def disable(self):
		result = self.send([self.getseq(), '0x1', '0x9'])
		return result

	def enable(self):
		result = self.send([self.getseq(), '0x1', '0xA'])
		
		return result

	# SSP_CMD_PROGRAM 0xB not implented

	def serial_number(self):
		result = self.send([self.getseq(), '0x1', '0xC'])
		
		serial = 0

		for i in range(4, 8):
			serial += int(result[i], 16) << (8 * (7-i) )	

		return serial

	def unit_data(self):
		result = self.send([self.getseq(), '0x1', '0xD'])

		fwversion = ''
		for i in range(5, 9):
			fwversion += chr(int(result[i], 16))

		country = ''
		for i in range(9, 12):
			country += chr(int(result[i], 16))

#		valuemulti = ''
#		for i in range(12, 15):
#			valuemulti += chr(int(result[i], 16))
# chr(int(0x0, 16)) returns \x00 instead of 0 - should be fixed somehow...

		unit_data = [int(result[4], 16), fwversion, country, int(result[14], 16), int(result[15], 16)]

		return unit_data

	def channel_values(self):
		result = self.send([self.getseq(), '0x1', '0xE'])
		return result

	def channel_security(self):
		result = self.send([self.getseq(), '0x1', '0xF'])
		return result

	def channel_reteach(self):
		result = self.send([self.getseq(), '0x1', '0xG'])
		return result

	def sync(self):
		#set ssp_sequence to 0x00, so next will be 0x80 by default
		self.__sequence = '0x00'
		
		result = self.send([self.getseq(), '0x1', '0x11'])
		
		return result

	# SSP_CMD_DISPENSE 0x12 not implented

	# SSP_CMD_PROGRAM_STATUS 0x16 not implented

	def last_reject(self):
		result = self.send([self.getseq(), '0x1', '0x17'])
		return result

	def hold(self):
		result = self.send([self.getseq(), '0x1', '0x18'])
		return result

	# SPP_CMD_MANUFACTURER 0x30 not implented - collides with SSP_CMD_EXPANSION ?!

	# SSP_CMD_EXPANSION 0x30 not implented - collides with SSP_CMD_MANUFACTURER ?!

	def enable_higher_protocol(self):
		result = self.send([self.getseq(), '0x1', '0x19'])
		return result
	
# End Of Definition Of SSP_CMD_* Commands

	def getseq(self):	
		# toggle SEQ between 0x80 and 0x00
		if ( self.__sequence == '0x80' ):
			self.__sequence = '0x00'
		else :
			self.__sequence = '0x80'
		
		returnseq = hex( self.__eSSPId | int(self.__sequence, 16) )
	
		return returnseq

	def crc(self, command):
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

	def send(self, command):
		crc = self.crc(command)
		
		prepedstring = '7F'

		command = command + crc

		for i in range(0, len(command)):
			if ( len(command[i]) % 2 == 1):
				prepedstring += '0'
		
			prepedstring += command[i][2:]
	
		prepedstring = prepedstring.decode('hex')

		self.__ser.write(prepedstring)
		
		response = self.read()
		
		return response
	
	def read(self):
		response = self.__ser.read(3)
		response += self.__ser.read(ord(response[2]) + 2)
		
		response = self.arrayify_response(response)
		
		return response

	def arrayify_response(self, response):
		array = []
		for i in range( 0, len(response) ):
			array += [hex(ord(response[i]))]
	
		return array
