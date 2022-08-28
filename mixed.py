from djitellopy import Tello as TelloPy
import cv2
import pygame
import numpy as np
import Button

# Creates window, go to fullscreen mode to fill
WIDTH = 800
HEIGHT = 600

# Reccomended numbers are 124, 16
BUTTON_WIDTH = 100
BUTTON_SPACING = 12

# Speed of the tello drone
SPEED = 60

pygame.init()

window = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Tello Inteface")

# Sets background color
window.fill((0, 0, 0))

# Updates screen
pygame.display.flip()

# Creates all the buttons on the screen
Buttons = []
# Creates left, right, up, down
Left = Button.Button(BUTTON_SPACING, HEIGHT-BUTTON_WIDTH-BUTTON_SPACING, "Images/Left.png", "Images/LeftDown.png", BUTTON_WIDTH)
Buttons.append(Left)
Backward = Button.Button(BUTTON_SPACING*2+BUTTON_WIDTH, HEIGHT-BUTTON_WIDTH-BUTTON_SPACING, "Images/Backward.png", "Images/BackwardDown.png", BUTTON_WIDTH)
Buttons.append(Backward)
Right = Button.Button(BUTTON_SPACING*3+BUTTON_WIDTH*2, HEIGHT-BUTTON_WIDTH-BUTTON_SPACING, "Images/Right.png", "Images/RightDown.png", BUTTON_WIDTH)
Buttons.append(Right)
Forward = Button.Button(BUTTON_SPACING*2+BUTTON_WIDTH, HEIGHT-BUTTON_WIDTH*2-BUTTON_SPACING*2, "Images/Forward.png", "Images/ForwardDown.png", BUTTON_WIDTH)
Buttons.append(Forward)

# Creates rotate left, rotate right, up and down
RotateRight = Button.Button(WIDTH-BUTTON_WIDTH-BUTTON_SPACING, HEIGHT-BUTTON_WIDTH-BUTTON_SPACING, "Images/rRight.png", "Images/rRightDown.png", BUTTON_WIDTH)
Buttons.append(RotateRight)
RotateLeft = Button.Button(WIDTH-BUTTON_WIDTH*3-BUTTON_SPACING*3, HEIGHT-BUTTON_WIDTH-BUTTON_SPACING, "Images/rLeft.png", "Images/rLeftDown.png", BUTTON_WIDTH)
Buttons.append(RotateLeft)
Down = Button.Button(WIDTH-BUTTON_WIDTH*2-BUTTON_SPACING*2, HEIGHT-BUTTON_WIDTH-BUTTON_SPACING, "Images/Down.png", "Images/DownDown.png", BUTTON_WIDTH)
Buttons.append(Down)
Up = Button.Button(WIDTH-BUTTON_WIDTH*2-BUTTON_SPACING*2, HEIGHT-BUTTON_WIDTH*2-BUTTON_SPACING*2, "Images/Up.png", "Images/UpDown.png", BUTTON_WIDTH)
Buttons.append(Up)

# Creates the special buttons, start flight, power off, connect
StartFlight = Button.Button(BUTTON_SPACING, BUTTON_SPACING, "Images/sFlight.png", "Images/sFlight.png", BUTTON_WIDTH)
Buttons.append(StartFlight)
EndFlight = Button.Button(BUTTON_SPACING*2+BUTTON_WIDTH*1, BUTTON_SPACING, "Images/eFlight.png", "Images/eFlight.png", BUTTON_WIDTH)
Buttons.append(EndFlight)

# Function to draw the buttons on the screen
def draw(button):
    if button.keyDown:
        window.blit(button.imgDown, (button.x, button.y))
    else:
        window.blit(button.img, (button.x, button.y))


# Creates the Tello object then connects to the drone
Tello = TelloPy()
Tello.connect(True)
Tello.set_speed(SPEED)

# Makes sure stream is off before restarting it
Tello.streamoff()
Tello.streamon()

# Gets video object from Tello Drone
frame_read = Tello.get_frame_read()

# Variable to keep our game loop running
running = True

# Keeps program from sending endless commands to Tello for no reason
sendNothing = False

# Main Loop
while running:
    # for loop through the event queue
    for e in pygame.event.get():
        # Check for QUIT event
        if e.type == pygame.QUIT:
            running = False

        # Gets when a key is pressed down
        if e.type == pygame.KEYDOWN:
            # Checks for the moving keys
            if e.key == pygame.K_s:
                Backward.keyDown = True
            if e.key == pygame.K_d:
                Right.keyDown = True
            if e.key == pygame.K_a:
                Left.keyDown = True
            if e.key == pygame.K_w:
                Forward.keyDown = True

            if e.key == pygame.K_k:
                Down.keyDown = True
            if e.key == pygame.K_l:
                RotateRight.keyDown = True
            if e.key == pygame.K_j:
                RotateLeft.keyDown = True
            if e.key == pygame.K_i:
                Up.keyDown = True

            # All the special keys, don't do anything unless "key up"
            if e.key == pygame.K_1:
                StartFlight.keyDown = True
            if e.key == pygame.K_2:
                EndFlight.keyDown = True

        # Gets when a key is let up
        if e.type == pygame.KEYUP:
            # All the moving keys
            if e.key == pygame.K_s:
                Backward.keyDown = False
            if e.key == pygame.K_d:
                Right.keyDown = False
            if e.key == pygame.K_a:
                Left.keyDown = False
            if e.key == pygame.K_w:
                Forward.keyDown = False

            if e.key == pygame.K_k:
                Down.keyDown = False
            if e.key == pygame.K_l:
                RotateRight.keyDown = False
            if e.key == pygame.K_j:
                RotateLeft.keyDown = False
            if e.key == pygame.K_i:
                Up.keyDown = False

            # All the special keys, Should call the command right here
            if e.key == pygame.K_1:
                StartFlight.keyDown = False
                Tello.takeoff()
            if e.key == pygame.K_2:
                EndFlight.keyDown = False
                Tello.land()

    # Sets vars for speed of right-left, up-down
    rl = 0
    ud = 0
    fb = 0
    yaw = 0

    if(Forward.keyDown):
        fb += SPEED
    if(Backward.keyDown):
        fb -= SPEED
    if(Right.keyDown):
        rl += SPEED
    if(Left.keyDown):
        rl -= SPEED

    if(Up.keyDown):
        ud += SPEED
    if(Down.keyDown):
        ud -= SPEED
    if(RotateRight.keyDown):
        yaw += SPEED
    if(RotateLeft.keyDown):
        yaw -= SPEED

    # Sends command to move the Tello if the tello should move
    if not sendNothing:
        Tello.send_rc_control(rl, fb, ud, yaw)
    if(rl==0 and fb==0 and ud==0 and yaw==0):
        sendNothing = True
    else:
        sendNothing = False

    # Show the display:
    # Show background frame
    frame = frame_read.frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = np.flipud(frame)

    frame = pygame.surfarray.make_surface(frame)
    window.blit(frame, (0, 0))

    # Show all the buttons on the screen
    for button in Buttons:
        draw(button)

    pygame.display.flip()

# Call to end drone process
Tello.end()