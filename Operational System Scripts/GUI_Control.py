import time
import os
import tkinter as tk
import Camera_Function as cf
import Motor_Function as mf
import Distance_sensor_Function as dsf
import Temp_Humid_Function as thf
import Measurement_Functions as mefu

# EXIT GUI Command
def exit_app():
        thf.dhtDevice.exit()
        root.destroy()
        cf.GPIO.cleanup(25)

# GUI Layout and function
root = tk.Tk()
root.title("Controls")

main_frame = tk.Frame(root, width=1000, height=1000)
main_frame.grid(row=0, column=0,padx=20,pady=20)

exit_button = tk.Button(main_frame, text="Exit", fg="red", font=("Arial",20), command=exit_app).grid(row=0,column=4)

# Message window
def display_message(message):
    text_widget.insert('end', message + '\n')
    text_widget.see('end')  # Auto-scroll to the end

#text_widget_label = tk.Label(main_frame, text= "System Messages:", font="Arial").grid(row=0,column=4,padx=5,pady=5)
text_widget = tk.Text(main_frame, height=20, width=10)
text_widget.grid(row=1, column=4)

#Manual motor control Frame
motor_control=tk.Frame(main_frame,width=500,height=500)
motor_control.grid(row=1,column=1, padx=1, pady=1)
#tk.Label(main_frame,text="Manual Motor Controls:", font="Arial").grid(row=0,column=1,padx=5,pady=5)

# Set Step Speed VERTICAL
def set_step_speed_vertical(event):
    mf.set_step_speed_vertical(speed_scale_vertical.get())
speed_label_vertical = tk.Label(motor_control, text="Vertical Speed Control (Fast --> Slow):").grid(row=0,column=0,padx=1,pady=1)
speed_scale_vertical = tk.Scale(motor_control, from_=0.0001, to=0.0009, resolution=0.0001, orient=tk.HORIZONTAL)
speed_scale_vertical.configure(length=200)
speed_scale_vertical.grid(row=0,column=1,padx=1,pady=1)
speed_scale_vertical.bind("<ButtonRelease-1>", set_step_speed_vertical)

# Set Step Speed ROTATE
def set_step_speed_rotate(event):
    mf.set_step_speed_rotate(speed_scale_rotate.get())
speed_label_rotate = tk.Label(motor_control, text="Rotate Speed Control (Fast --> Slow):").grid(row=3,column=0,padx=1,pady=1)
speed_scale_rotate = tk.Scale(motor_control, from_=0.001, to=0.002, resolution=0.0001, orient=tk.HORIZONTAL,length=100)
speed_scale_rotate.configure(length=200)
speed_scale_rotate.grid(row=3,column=1,padx=1,pady=1)
speed_scale_rotate.bind("<ButtonRelease-1>", set_step_speed_rotate)

# Create the vertical motor control frame
def set_steps_vertical(event):
    mf.set_steps_vertical(vertical_steps_entry.get())
vertical_direction_button = tk.Button(motor_control, text="Down", command=lambda: mf.move_vertical_DOWN(mf.num_steps_vertical)).grid(row=2,column=0,padx=1,pady=1)
vertical_direction_button = tk.Button(motor_control, text="Up", command=lambda: mf.move_vertical_UP(mf.num_steps_vertical)).grid(row=2,column=1,padx=1,pady=1)
vertical_steps_label = tk.Label(motor_control, text="Vertical Steps (1cm = 800 steps): ").grid(row=1,column=0,padx=10,pady=10)
vertical_steps_entry = tk.Entry(motor_control)
vertical_steps_entry.grid(row=1,column=1,padx=1,pady=1)
vertical_steps_entry.bind("<KeyRelease>", set_steps_vertical)

# Create the rotate motor control frame
def set_steps_horizontal(event):
    mf.set_steps_horizontal(horizontal_steps_entry.get())
horizontal_direction_button = tk.Button(motor_control, text="Left", command=lambda:mf.rotate_LEFT(mf.num_steps_horizontal)).grid(row=5,column=0,padx=1,pady=1)
horizontal_direction_button = tk.Button(motor_control, text="Right", command=lambda: mf.rotate_RIGHT(mf.num_steps_horizontal)).grid(row=5,column=1,padx=1,pady=1)
horizontal_steps_label = tk.Label(motor_control, text=" Horizontal Steps (1cm = 408 steps): ").grid(row=4,column=0,padx=10,pady=10)
horizontal_steps_entry = tk.Entry(motor_control)
horizontal_steps_entry.grid(row=4,column=1,padx=1,pady=1)
horizontal_steps_entry.bind("<KeyRelease>", set_steps_horizontal)

#Move "HOME" 
home_button = tk.Button(motor_control, text="Move to Bottom Position", command=mf.move_home).grid(row=6,column=0,padx=10,pady=10)

#Move to top
top_button = tk.Button(motor_control, text="Move to the Top Position", command=mf.move_top).grid(row=6,column=1,padx=10,pady=10)


## Move to Distance - WORK IN PROGRESS ##
#def set_distance(distance_trigger):
   # global new_distance_value
   # global current_distance_value
   # new_distance_value = move_distance_entry.get()
   # current_distance_value = dsf.median_distance

#move_distance_button = tk.Button(motor_control, text="Move to Distance", command=lambda: mf.move_distance(new_distance_value,current_distance_value)).grid(row=7,column=0,padx=10,pady=10)
#move_distance_entry = tk.Entry(motor_control)
#move_distance_entry.grid(row=7,column=1,padx=10,pady=10)
#move_distance_entry.bind("<KeyRelease>", set_distance)

# Distance Sensor
distance_label = tk.Label(motor_control, text="Distance from Bottom: ")
distance_label.grid(row=8,column=0,padx=10,pady=10)
#dsf.measure_distance(distance_label)

# Temperature and humidity 
temp_humid_frame = tk.Frame(main_frame,width=100,height=100)
temp_humid_frame.grid(row=5,column=4,padx=1,pady=1)
temp_label = tk.Label(temp_humid_frame, text="Temperature:")
temp_label.grid(row=1,column=1,padx=1,pady=1)
humidity_label = tk.Label(temp_humid_frame, text="Humidity:")
humidity_label.grid(row=1,column=4,padx=1,pady=1)
thf.update_temp_values(temp_label, humidity_label)

# Camera functions
camera_frame = tk.Frame(main_frame, width=200,height=500)
camera_frame.grid(row=1,column=2,padx=10,pady=10)
#camera_frame_title = tk.Label(main_frame, text= "Camera Functions:",font="Arial").grid(row=0,column=2,padx=5,pady=5)
preview_button = tk.Button(camera_frame, text="Start Live Preview", command=cf.start_preview).grid(row=1,column=0,padx=5,pady=5)
stop_preview_button = tk.Button(camera_frame,text="Stop Live Preview", command=cf.stop_preview).grid(row=1,column=1,padx=5,pady=5)
camera_jpeg_button = tk.Button(camera_frame, text="Capture JPEG Image", command= cf.capture_jpeg).grid(row=2,column=0,padx=5,pady=5)
camera_raw_button = tk.Button(camera_frame, text="Capture RAW Image", command=lambda: cf.capture_raw(exposure_time, iso_value)).grid(row=6,column=0,padx=1,pady=1)
camera_raw_background_button = tk.Button(camera_frame, text="RAW image (UV-LED OFF)", command=lambda: cf.capture_raw_background(exposure_time, iso_value)).grid(row=6,column=1,padx=1,pady=1)


# Camera Settings: Exposure and ISO
def set_exposure(exposure):
     global exposure_time
     exposure_time_get = exposure_entry.get() 
     exposure_time = int(float(exposure_time_get) * 10E5)
     display_message(f"exposure: {exposure_time}\n")
     

exposure_label = tk.Label(camera_frame, text= "Exposure Time (seconds):").grid(row=3,column=0,padx=1,pady=1)     
exposure_entry = tk.Entry(camera_frame)
exposure_entry.grid(row=3,column=1,padx=1,pady=1)
exposure_entry.bind("<KeyRelease>", set_exposure)

def set_iso(iso):
     global iso_value
     iso_value_get = iso_entry.get()
     iso_value = int(iso_value_get)
     display_message(f"ISO: {iso_value}\n")

iso_label = tk.Label(camera_frame, text= "ISO:").grid(row=4,column=0,padx=1,pady=1)
iso_entry = tk.Entry(camera_frame)
iso_entry.grid(row=4,column=1,padx=1,pady=1)
iso_entry.bind("<KeyRelease>", set_iso)

#UV LED Control
def toggle_uv_state():
    global uv_state
    if uv_label.cget("text") == "ON":
        uv_label.config(text="OFF")
        cf.GPIO.output(cf.led, cf.GPIO.LOW)
    else:
        uv_label.config(text="ON")
        cf.GPIO.output(cf.led, cf.GPIO.HIGH)
    
    uv_state = uv_label.cget("text") == "ON"

    display_message(f"UV state: {uv_state}\n")
    
uv_label = tk.Label(camera_frame,text="OFF")
uv_label.grid(row=5,column=1,padx=5,pady=5)
uv_button =tk.Button(camera_frame,text="Toggle UV LED:", command=toggle_uv_state).grid(row=5,column=0,padx=5,pady=5)

#White LED Control
def toggle_white_led_state():
    global white_state
    if white_label.cget("text") == "ON":
        white_label.config(text="OFF")
        cf.GPIO.output(cf.white_led, cf.GPIO.LOW)
    else:
        white_label.config(text="ON")
        cf.GPIO.output(25,cf.GPIO.HIGH)
    
    white_state = white_label.cget("text") == "ON"

    display_message(f"White LED state: {white_state}\n")
    
white_label = tk.Label(camera_frame,text="OFF")
white_label.grid(row=0,column=1,padx=5,pady=5)
white_button =tk.Button(camera_frame,text="Toggle White LED:", command=toggle_white_led_state).grid(row=0,column=0,padx=5,pady=5)

#Show Histogram 
histogram_button = tk.Button(camera_frame, text= " Histogram + Column Ratio ", command=cf.display_histogram).grid(row=7,column=0, padx=1,pady=1 )

#Capture Calibration images 

def set_o2(o2_trigger):
    global o2_value
    o2_value = o2_entry.get()
    display_message(f"O2 %: {o2_value}\n")
    
def set_image_number(image_number_trigger):
    global num_images
    num_images = int(num_images_entry.get())
    display_message(f"number of images: {num_images}\n")

def set_delay(delay_trigger):
    global delay_time
    delay_time = int(delay_time_entry.get())
    display_message(f"Delay time: {delay_time}\n")

def capture_calibration_images():
    cf.capture_calibration(o2_value, num_images, exposure_time, iso_value, delay_time)
    display_message("Image Sequence Completed.\n")

o2_label = tk.Label(camera_frame, text="Set Image Name:").grid(row=11,column=0,padx=1,pady=1)
o2_entry = tk.Entry(camera_frame)
o2_entry.grid(row=11,column=1,padx=1,pady=1)
o2_entry.bind("<KeyRelease>", set_o2)
delay_time_label = tk.Label(camera_frame, text="Set Delay Between Images:").grid(row=10,column=0,padx=1,pady=1)
delay_time_entry = tk.Entry(camera_frame)
delay_time_entry.grid(row=10,column=1,padx=1,pady=1)
delay_time_entry.bind("<KeyRelease>", set_delay)
num_images_label = tk.Label(camera_frame, text="Enter Number of Images:").grid(row=9,column=0, padx=1,pady=1 )
num_images_entry = tk.Entry(camera_frame)
num_images_entry.grid(row=9,column=1, padx=1,pady=1 )
num_images_entry.bind("<KeyRelease>", set_image_number)
capture_calibration_button = tk.Button(camera_frame, text="Capture Image Sequence", command=capture_calibration_images).grid(row=12,column=0,padx=10,pady=10)
capture_calibration_label = tk.Label(camera_frame,text="Sequence Settings:", font=8).grid(row=8,column=0,padx=10,pady=10)


#Measurements Sequence

#Camera field of view in cm
fov_x = 3.6 
fov_y = 2.7
#Camera field of view in steps
fov_x_steps = round(fov_x * 407.5)
fov_y_steps = round(fov_y * 800)

def measurement_direction():
    global direction
    if measurement_direction_vertical_label.cget("text") == "UP":
       measurement_direction_vertical_label.config(text="DOWN")
       direction = False
    else:
       measurement_direction_vertical_label.config(text="UP")
       direction = True

    message = f"Direction_state: {direction}\n"
    text_widget.insert('end', message)
    text_widget.see('end')

def set_horizontal_step_range(hori_range_trigger):
    global hori_range
    hori_range_get = int(horizontal_view_entry.get())
    if hori_range_get < 1:
        message = f"Horizontal range must be at least 1\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    elif hori_range_get == 1:
        hori_range = 0 
        message = f"Horizontal Step Range: {hori_range}\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    else:
        hori_range = round(hori_range_get * fov_x_steps)
        message = f"Horizontal Step Range: {hori_range}\n"
        text_widget.insert('end', message)
        text_widget.see('end')
     
def set_verticale_step_range(vert_range_trigger):
    global vert_range
    vert_range_get = int(vertical_view_entry.get())
    if vert_range_get < 1:
        message = f"Vertical range must be at least 1\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    elif vert_range_get ==1:
        vert_range = 0
        message = f"Vertical Step Range: {vert_range}\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    else:
        vert_range = round(vert_range_get * fov_y_steps)
        message = f"Vertical Step Range: {vert_range}\n"
        text_widget.insert('end', message)
        text_widget.see('end')


def set_horizontal_overlap(hori_overlap_trigger):
    global hori_overlap
    hori_overlap_get = int(horizontal_overlap_entry.get())
    if hori_overlap_get > 99:
        message = f"Maximum 99% overlap\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    elif hori_overlap_get == 0:
        hori_overlap = fov_x_steps
        message = f"Horizontal Step Overlap: {hori_overlap}\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    else:
        hori_overlap = round(fov_x_steps * (100 - hori_overlap_get) / 100)

        message = f"Horizontal Step Overlap: {hori_overlap}\n"
        text_widget.insert('end', message)
        text_widget.see('end')

def set_vertical_overlap(vert_overlap_trigger):
    global vert_overlap
    vert_overlap_get = int(vertical_overlap_entry.get())
    if vert_overlap_get > 99:
        message = f"Maximum 99% overlap\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    elif vert_overlap_get == 0:
        vert_overlap = fov_y_steps
        message = f"vertical Step Overlap: {vert_overlap}\n"
        text_widget.insert('end', message)
        text_widget.see('end')
    else:
        vert_overlap = round(fov_y_steps * (100 - vert_overlap_get) / 100)
        message = f"Vertical Step Overlap: {vert_overlap}\n"
        text_widget.insert('end', message)
        text_widget.see('end')

def image_range():
    global hori_image_range
    global vert_image_range
    global num_images_seq
    hori_image_range = round(hori_range/hori_overlap)
    vert_image_range = round(vert_range/vert_overlap)
    if hori_image_range == 0:
        hori_image_range = 1
        num_images_seq = vert_image_range
    else:
        num_images_seq = round(hori_image_range * vert_image_range)
    number_images_sequence.config(text="Number of Images in Sequence:{} - Vertical:{} - Horizontal:{}".format(num_images_seq, vert_image_range,hori_image_range))
    print(hori_image_range)
    print(vert_image_range)

def set_seqeunce_number(seq_num_trigger):
    global seq_num
    seq_num = int(sequence_number_entry.get())


# Add a variable to track the number of times the sequence has run
sequence_count = 0

# Define the path to the desktop
desktop_path = os.path.expanduser("~/Desktop")

# Ensure the desktop directory exists (it should already exist on the Raspberry Pi)
os.makedirs(desktop_path, exist_ok=True)

def run_measurement_sequence():
    global sequence_count

    # Get the total number of sequences and sequence delay from the input fields
    total_sequences = int(total_sequences_entry.get())
    sequence_delay = int(sequence_delay_entry.get())

    # Record the start time
    start_time = time.time()

    # Run the measurement sequence logic
    mefu.measurement_sequence(vert_image_range, hori_image_range, vert_overlap, hori_overlap, direction, exposure_time, iso_value, seq_num)
    
    # Call the function to move the camera back to initial position
    mefu.move_to_initial_position(vert_image_range, hori_image_range, vert_overlap, direction, hori_overlap)

    # Retrieve the temperature, and humidity from the GUI labels
    temperature_text = temp_label.cget("text")
    humidity_text = humidity_label.cget("text")

    # Extract numeric values from the text
    try:
        temperature = float(temperature_text.split(" ")[1])  # Get the value after "Temperature"
        humidity = float(humidity_text.split(" ")[1].replace("%", ""))  # Get the value after "Humidity"
    except (IndexError, ValueError):
        temperature = "N/A"
        humidity = "N/A"

    # Construct the log file path on the desktop
    log_file_path = os.path.join(desktop_path, "measurement_log.txt")

    # Log the data to a TXT file
    with open(log_file_path, mode="a") as file:
        # Write header if it's the first sequence
        if sequence_count == 0:
            file.write("Sequence Number | Temperature (°C) | Humidity (%) | Timestamp\n")
            file.write("-" * 70 + "\n")
        
        # Write the data
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.write(f"{sequence_count + 1:>15} | {temperature:>16} | {humidity:>12} | {timestamp}\n")

    # Increment the sequence count
    sequence_count += 1
    print(f"Completed sequence {sequence_count}\n")

    # Record the end time and calculate execution time
    execution_time = time.time() - start_time
    print(execution_time)

    # Calculate remaining delay time
    remaining_delay = max(0, sequence_delay - execution_time)

    # Check if the desired number of sequences have run
    if sequence_count < total_sequences:
        print(f"Waiting for {remaining_delay:.2f} seconds before starting the next sequence...\n")
        time.sleep(remaining_delay)

        # Call the function recursively to run the next sequence
        run_measurement_sequence()
    else:
        print("All sequences completed!\n")


# Function to start the measurement sequence
def start_measurement():
    global sequence_count

    # Reset sequence count before starting
    sequence_count = 0

    # Call the function to run the measurement sequence
    run_measurement_sequence()

def set_sequence_number(seq_num_trigger):
    global seq_num
    seq_num = int(sequence_number_entry.get())


mearsurement_frame = tk.Frame(main_frame,width=200,height=500)
mearsurement_frame.grid(row=1,column=3,padx=1,pady=1)
mearsurement_frame_title = tk.Label(main_frame, text="Measurement Sequence:",font="Arial").grid(row=0,column=3,padx=5,pady=5)
horizontal_view_label = tk.Label(mearsurement_frame,text="Set horizontal Frames (1 = 3.6 cm):").grid(row=0,column=0,padx=1,pady=1)
horizontal_view_entry = tk.Entry(mearsurement_frame)
horizontal_view_entry.grid(row=0,column=1,padx=5,pady=5)
horizontal_view_entry.bind("<KeyRelease>", set_horizontal_step_range)
vertical_view_label = tk.Label(mearsurement_frame,text="Set vertical Frames (1 = 2.7 cm):").grid(row=1,column=0,padx=1,pady=1)
vertical_view_entry = tk.Entry(mearsurement_frame)
vertical_view_entry.grid(row=1,column=1,padx=5,pady=5)
vertical_view_entry.bind("<KeyRelease>",set_verticale_step_range)
horizontal_overlap_label = tk.Label(mearsurement_frame,text="Set Horizontal Image Overlap %:").grid(row=2,column=0,padx=1,pady=1)
horizontal_overlap_entry = tk.Entry(mearsurement_frame)
horizontal_overlap_entry.grid(row=2,column=1,padx=5,pady=5)
horizontal_overlap_entry.bind("<KeyRelease>",set_horizontal_overlap)
vertical_overlap_label = tk.Label(mearsurement_frame,text="Set Vertical Image Overlap %:").grid(row=3,column=0,padx=1,pady=1)
vertical_overlap_entry = tk.Entry(mearsurement_frame)
vertical_overlap_entry.grid(row=3,column=1,padx=5,pady=5)
vertical_overlap_entry.bind("<KeyRelease>", set_vertical_overlap)
measurement_direction_vertical_label = tk.Label(mearsurement_frame, text="DOWN")
measurement_direction_vertical_label.grid(row=4,column=1,padx=5,pady=5)
measurement_direction_vertical_button = tk.Button(mearsurement_frame,text="Vertical Measurement Direction:", command=measurement_direction).grid(row=4,column=0,padx=5,pady=5)
confirm_button = tk.Button(mearsurement_frame,text="Confirm Image Range", command=image_range).grid(row=5,column=0,padx=5,pady=5)
number_images_sequence = tk.Label(mearsurement_frame, text="Number of Images in Sequence:")
number_images_sequence.grid(row=6,column=0,padx=5,pady=5)
sequence_number_label = tk.Label(mearsurement_frame,text="Set Sequence Nametag (Number):").grid(row=7,column=0,padx=5,pady=5)
sequence_number_entry = tk.Entry(mearsurement_frame)
sequence_number_entry.grid(row=7,column=1,padx=5,pady=5)
sequence_number_entry.bind("<KeyRelease>", set_seqeunce_number)
total_sequences_label = tk.Label(mearsurement_frame, text=" Repeat Sequence:")
total_sequences_label.grid(row=8, column=0, padx=5, pady=5)
total_sequences_entry = tk.Entry(mearsurement_frame)
total_sequences_entry.grid(row=8, column=1, padx=5, pady=5)
sequence_delay_label = tk.Label(mearsurement_frame, text="Delay Between Sequences (seconds):")
sequence_delay_label.grid(row=9, column=0, padx=5, pady=5)
sequence_delay_entry = tk.Entry(mearsurement_frame)
sequence_delay_entry.grid(row=9, column=1, padx=5, pady=5)

start_measure_button = tk.Button(mearsurement_frame,text="Start Measurement Sequence", command=start_measurement).grid(row=10,column=0,padx=5,pady=5)
#stop_measure_button = tk.Button(mearsurement_frame,text="Stop Measurement Sequence").grid(row=8,column=1,padx=5,pady=5)

# Start GUI
root.mainloop()


     
