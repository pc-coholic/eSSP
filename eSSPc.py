import serial
import logging

LOG_FILENAME = 'logs/eSSP.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

class eSSPc(object):
	def __init__(self, serialport = '/dev/ttyUSB0', eSSPId = 0):
		self.__ser = serial.Serial(serialport, 9600)
		self.__eSSPId = eSSPId
		self.__sequence = '0x80'
		
	def sync(self):
		#set ssp_sequence to 0x00, so next will be 0x80 by default
		self.__sequence = '0x00'
		
		result = self.send([getseq(), '0x1', '0x11'])
		
		return result

	def serial_number(self):
		result = self.send([getseq(), '0x1', '0xC'])
		
		serial = 0

		for i in range(4, 8):
			serial += int(result[i], 16) << (8 * (7-i) )	

		return serial

	def getseq():	
		# toggle SEQ between 0x80 and 0x00
		if ( self.__sequence == '0x80' ):
			self.__sequence = '0x00'
		else :
			self.__sequence = '0x80'
		
		returnseq = hex( ssp_address | int(ssp_sequence, 16) )
	
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
		
		return prepedstring
	
	def read(self):
		response = ser.read(3)
		response += ser.read(ord(response[2]) + 2)
		
		response = self.arrayify_response(response)
		
		return response

	def arrayify_response(response):
		array = []
		for i in range( 0, len(response) ):
			array += [hex(ord(response[i]))]
	
		return array
