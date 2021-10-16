import pygame, time
pygame.init()

HORIZONTAL, VERTICAL = 0, 1

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
	joystick.init()

# Joystick axis values:
# 0 - horizontal, positive is right
# 1 - vertical, positive is down

joystick_values = {0:0, 1:0, 2:0, 3:0}

while True:
	for event in pygame.event.get():
		if event.type == pygame.JOYAXISMOTION:
			if(abs(event.value) > .1 ):
				joystick_values[event.axis] = event.value
			else:
				joystick_values[event.axis] = 0
			
			output = []
			string = ""
			
			if(joystick_values[HORIZONTAL] >= 0):
				string += "f"
			else:
				string += "r"
			
			string += str(int(joystick_values[HORIZONTAL] * 255))
			
			output.append(string)
			output.append(string)
			
			print(output)
		
	time.sleep(0.2)