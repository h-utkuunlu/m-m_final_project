import serial
from time import sleep
ser = serial.Serial('/dev/ttyACM0', 57600)

while True:

	ser.write('1'.encode())
	print("1")
	sleep(0.5)
	ser.write('3'.encode())
	print("3")
	sleep(0.5)
	ser.write('0'.encode())
	print("0")
	sleep(0.5)
	ser.write('2'.encode())
	print("2")
	sleep(0.5)
