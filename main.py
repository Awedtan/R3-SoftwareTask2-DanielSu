import pygame, time, math
pygame.init()

HORIZONTAL, VERTICAL = 0, 1
DEADZONE = 0.2

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
	joystick.init()

# Joystick axis values:
# 0 - horizontal, positive is right
# 1 - vertical, positive is down

joystick_values = {0:0, 1:0, 2:0, 3:0}

while True:
	
	isMoving = False
	
	for event in pygame.event.get():
		if event.type == pygame.JOYAXISMOTION:
			if(abs(event.value) > DEADZONE ):
				joystick_values[event.axis] = event.value
			else:
				joystick_values[event.axis] = 0
	
	
	for key in joystick_values:
		if joystick_values[key] != 0:
			isMoving = True
	
	right = joystick_values[0] >= DEADZONE
	forward = -joystick_values[1] >= DEADZONE
	
	print(joystick_values)
	print(isMoving)
	print("r:" + str(right))
	print("f:" + str(forward))
	print()
	
	motor_out = ["0", "0", "0", "0"]
	
	if(not isMoving):
		continue
	
	magnitude = math.sqrt(joystick_values[0]**2 + joystick_values[1]**2)
	if(magnitude > 1):
		magnitude = 1
	
	speed = int(magnitude*255)
	
	if right:
		if forward:
			motor_out[0] = "f255"
			# motor_out[2] = something
		else:
			# motor_out[0] = something
			motor_out[2] = "r255"
	elif forward:
		# motor_out[0] = something
		motor_out[2] = "f255"
	else:
		motor_out[0] = "r255"
		# motor_out[2] = something
	
	motor_out[1] = motor_out[0]
	motor_out[3] = motor_out[2]
	
	print(motor_out)
		
	time.sleep(0.4)