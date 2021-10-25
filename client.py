# Daniel Su, October 24, R3 Software Task 2
# Client program, receives joystick input and sends to server

import socket, json, pygame, time

pygame.init() # Initialize pygame, which is used for joystick input
DEADZONE = 0.1 # Joystick deadzone
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())] # Gets all conencted joysticks
for joystick in joysticks:
	joystick.init() # Initialize all connected joysticks

IP = '127.0.0.1' # Localhost IP address
PORT = 5005 # Port to connect to
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT)) # Connect to the server

# Joystick axis values:
# 0 - horizontal, positive is right
# 1 - vertical, positive is down
joystick_values = {0: 0, 1: 0}

while True:
	for event in pygame.event.get():
		if event.type == pygame.JOYAXISMOTION: # Wait for joystick movement
			if(abs(event.value) > DEADZONE):
				joystick_values[event.axis] = event.value # Joystick is moved beyond the deadzone
			else:
				joystick_values[event.axis] = 0 # Joystick is not moved beyond the deadzone
	
	# Check if the joystick is not in a neutral position
	isMoving = False
	for key in joystick_values:
		if joystick_values[key] != 0:
			isMoving = True

	if(not isMoving):
		continue

	MESSAGE = json.dumps(joystick_values).encode() # Serialize the dictionary of joystick axis values
	s.send(MESSAGE) # Send the joystick values to the server
	time.sleep(0.1)