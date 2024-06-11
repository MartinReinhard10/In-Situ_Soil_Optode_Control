import RPi.GPIO as GPIO
import time

# Set up GPIO pins in BCM mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define pin numbers for each motor
VERTICAL_STEP_PIN = 27
VERTICAL_DIR_PIN = 17
TOP_ENDSTOP_PIN = 19
BOTTOM_ENDSTOP_PIN = 21
ROTATE_STEP_PIN = 9
ROTATE_DIR_PIN = 10

# Set up pins as outputs
GPIO.setup(VERTICAL_STEP_PIN, GPIO.OUT)
GPIO.setup(VERTICAL_DIR_PIN, GPIO.OUT)
GPIO.setup(ROTATE_STEP_PIN, GPIO.OUT)
GPIO.setup(ROTATE_DIR_PIN, GPIO.OUT)

# Set up endstops as inputs
GPIO.setup(TOP_ENDSTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOTTOM_ENDSTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set motor direction
DOWN = GPIO.HIGH
UP = GPIO.LOW
LEFT = GPIO.LOW
RIGHT = GPIO.HIGH

# Move motor in steps
def step_vertical(step_pin):
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(step_speed_vertical)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(step_speed_vertical)

def step_rotate(step_pin):
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(step_speed_rotate)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(step_speed_rotate)


# Move vertical motor UP a certain number of steps or until an endstop is triggered
def move_vertical_UP(steps):
    GPIO.output(VERTICAL_DIR_PIN, UP)
    for i in range(steps):
        if  GPIO.input(TOP_ENDSTOP_PIN) == GPIO.LOW:
            print("Top endstop reached")
            break
        step_vertical(VERTICAL_STEP_PIN)

# Move vertical motor DOWN a certain number of steps or until an endstop is triggered
def move_vertical_DOWN(steps):
    GPIO.output(VERTICAL_DIR_PIN, DOWN)
    for i in range(steps):
        if  GPIO.input(BOTTOM_ENDSTOP_PIN) == GPIO.LOW:
            print("Bottom endstop reached")
            break
        step_vertical(VERTICAL_STEP_PIN)

# Rotate motor LEFT a certain number of steps
def rotate_LEFT(steps):
    GPIO.output(ROTATE_DIR_PIN, LEFT)
    for i in range(steps):
        step_rotate(ROTATE_STEP_PIN)
    
# Rotate motor RIGHT a certain number of steps
def rotate_RIGHT(steps):
    GPIO.output(ROTATE_DIR_PIN, RIGHT)
    for i in range(steps):
        step_rotate(ROTATE_STEP_PIN)

# Set the number of steps for VERTICAL
def set_steps_vertical(steps_v):
    global num_steps_vertical
    num_steps_vertical = int(steps_v)

# Set the number of steps for HORIZONTAL
def set_steps_horizontal(steps_h):
    global num_steps_horizontal
    num_steps_horizontal = int(steps_h)

# Set the step speed VERTICAL
def set_step_speed_vertical(speed_vertical):
    global step_speed_vertical
    step_speed_vertical = speed_vertical

# Set the step speed ROTATE
def set_step_speed_rotate(speed_rotate):
    global step_speed_rotate
    step_speed_rotate = speed_rotate

#Move HOME, Bottom position
def move_home():
    GPIO.output(VERTICAL_DIR_PIN, DOWN)
    while GPIO.input(BOTTOM_ENDSTOP_PIN) == GPIO.HIGH:
        step_vertical(VERTICAL_STEP_PIN)

# Move top position 
def move_top():
    GPIO.output(VERTICAL_DIR_PIN, UP)
    while GPIO.input(TOP_ENDSTOP_PIN) == GPIO.HIGH:
        step_vertical(VERTICAL_STEP_PIN)

# Move to set distance
def move_distance(new_distance, current_distance):
    if new_distance >= current_distance:
        GPIO.output(VERTICAL_DIR_PIN, UP)
    else:
        GPIO.output(VERTICAL_DIR_PIN, DOWN)
    while new_distance != current_distance and GPIO.input(BOTTOM_ENDSTOP_PIN) == GPIO.HIGH and GPIO.input(TOP_ENDSTOP_PIN) == GPIO.HIGH:
        step(VERTICAL_STEP_PIN)
        
    


