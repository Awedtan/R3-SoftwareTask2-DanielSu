# Daniel Su, October 24, R3 Software Task 2
# Server program, receives joystick input from client and outputs motor PWM values

import socket, json, math

HORIZONTAL, VERTICAL = '0', '1' # Keys for the joystick axis value dictionary
DEADZONE = 0.1 # Joystick deadzone

IP = '127.0.0.1' # Localhost IP address
PORT = 5005 # Port to connect to
BUFFER = 1024 # Buffer size

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT)) # Connect to the address and port
s.listen(1) # Enable receiving data
conn, addr = s.accept() # Connect to the client

while True:
	data = conn.recv(BUFFER) # Receive data from the client
	if not data: break
	
	joystick_values = json.loads(data) # Deserialize the data
	
	
	right = joystick_values[HORIZONTAL] >= DEADZONE # If the joystick is pointing right
	forward = -joystick_values[VERTICAL] >= DEADZONE # If the joystick is pointing forward

	motor_out = ['0', '0', '0', '0'] # Output array

	# The speed of the motors will be controlled by the joystick's displacment
	# The further the joystick is pushed, the greater the motor speeds will be
	# Ranges from 0 to 1
	magnitude = math.sqrt(joystick_values[HORIZONTAL]**2 + joystick_values[VERTICAL]**2) # Find the distance of the joystick to its neutral position, pythagoras
	if(magnitude > 1):
		magnitude = 1 # Magnitude can only be from 0-1
	speed = int(magnitude*255) # Maximum possible speed of a motor

	# The angle of the joystick is measured in radians from the x axis
	# Ranges from 0 to pi/2
	angle = 1
	if(joystick_values[HORIZONTAL] != 0): # Prevents division by zero
		angle = (abs(math.atan(joystick_values[VERTICAL]/joystick_values[HORIZONTAL])) - math.pi/4) / (math.pi/4) # Calculates the angle of the joystick

	# Calculate motor speeds based on joystick angle and displacement
	if right:
		# Moving forward and right
		if forward:
			motor_out[0] = 'f' + str(speed)
			right_speed = int(angle * speed)
			motor_out[2] = '{sign}{int}'.format(sign = 'f' if right_speed >= 0 else 'r', int = str(abs(right_speed)))

		# Moving backward and right
		else:
			left_speed = int(angle * speed)
			motor_out[0] = '{sign}{int}'.format(sign = 'r' if left_speed >= 0 else 'f', int = str(abs(left_speed)))
			motor_out[2] = 'r' + str(speed)

	# Moving forward and left
	elif forward:
		left_speed = int(angle * speed)
		motor_out[0] = '{sign}{int}'.format(sign = 'f' if left_speed >= 0 else 'r', int = str(abs(left_speed)))
		motor_out[2] = 'f' + str(speed)

	# Moving backward and left
	else:
		motor_out[0] = 'r' + str(speed)
		right_speed = int(angle * speed)
		motor_out[2] = '{sign}{int}'.format(sign = 'r' if right_speed >= 0 else 'f', int = str(abs(right_speed)))

	for x in range(1,4,2): # Copies motor speeds on the same side
		motor_out[x] = motor_out[x-1]

	print(motor_out)