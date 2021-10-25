import pygame, time, math
pygame.init()

HORIZONTAL, VERTICAL = 0, 1
DEADZONE = 0.1

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
	joystick.init()

# Joystick axis values:
# 0 - horizontal, positive is right
# 1 - vertical, positive is down

joystick_values = {0: 0, 1: 0, 2: 0, 3: 0}

while True:

	isMoving = False

	for event in pygame.event.get():
		if event.type == pygame.JOYAXISMOTION:
			if(abs(event.value) > DEADZONE):
				joystick_values[event.axis] = event.value
			else:
				joystick_values[event.axis] = 0

	for key in joystick_values:
		if joystick_values[key] != 0:
			isMoving = True

	right = joystick_values[0] >= DEADZONE
	forward = -joystick_values[1] >= DEADZONE

	# print(joystick_values)
	# print(isMoving)
	# print("r:" + str(right))
	# print("f:" + str(forward))
	# print()

	motor_out = ["0", "0", "0", "0"]

	if(not isMoving):
		continue

	magnitude = math.sqrt(joystick_values[0]**2 + joystick_values[1]**2)
	if(magnitude > 1):
		magnitude = 1
	speed = int(magnitude*255)

	angle = 1
	if(joystick_values[0] != 0):
		angle = (abs(math.atan(joystick_values[1]/joystick_values[0])) - math.pi/4) / (math.pi/4)

	if right:
		if forward:
			motor_out[0] = "f" + str(speed)

			temp = int(angle * speed)
			motor_out[2] = "f" if temp >= 0 else "r"
			motor_out[2] += str(abs(temp))

		else:
			temp = int(angle * speed)
			motor_out[0] = "r" if temp >= 0 else "f"
			motor_out[0] += str(abs(temp))

			motor_out[2] = "r" + str(speed)

	elif forward:
		temp = int(angle * speed)
		motor_out[0] = "f" if temp >= 0 else "r"
		motor_out[0] += str(abs(temp))

		motor_out[2] = "f" + str(speed)

	else:
		motor_out[0] = "r" + str(speed)

		temp = int(angle * speed)
		motor_out[2] = "r" if temp >= 0 else "f"
		motor_out[2] += str(abs(temp))

	for x in range(1,4,2):
		motor_out[x] = motor_out[x-1]

	print(motor_out)

	time.sleep(0.4)
