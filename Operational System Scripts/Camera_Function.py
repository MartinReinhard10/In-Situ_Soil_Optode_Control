from picamera2 import Picamera2, Preview
from picamera2.controls import Controls
from libcamera import Transform
import RPi.GPIO as GPIO
import tifffile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import numpy as np
from datetime import datetime
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set LED Pin
led = 23
GPIO.setup(led, GPIO.OUT)
white_led = 25
GPIO.setup(25,GPIO.OUT)

# Intialize Camera for preview and RGB image
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(
    main={"size": (4056, 3040)},
    lores={"size": (640, 480)},
    display="lores",
    transform=Transform(hflip=1, vflip=1),
)
picam2.configure(camera_config)


# Preview
def start_preview():
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()


def stop_preview():
    picam2.stop_preview()
    picam2.stop()


# Capture single JPEG image
def capture_jpeg():
    picam2.start()
    image = picam2.capture_image()
    picam2.stop_preview()
    picam2.stop()
    
    # Save the image to a file
    save_dir = '/home/martinoptode/Desktop/'  # Specify the directory where you want to save the image
    filename = 'captured_image.jpg'  # Specify the filename
    image.save(os.path.join(save_dir, filename))
    print("Image saved:", os.path.join(save_dir, filename))
    

# Capture single RAW image
def capture_raw(exposure, iso):
    global raw
    # Set camera controls
    controls = {"ExposureTime": exposure, #microseconds
            "AnalogueGain": iso, # 1 = ISO 100
            "AeEnable": False, # Auto exposure and Gain
            "AwbEnable": False,# Auto white Balance
            "FrameDurationLimits": (114,239000000)} #Min/Max frame duration
    # Setup config parameters
    preview_config = picam2.create_preview_configuration(raw={"size": picam2.sensor_resolution, "format": "SBGGR12",},
                                                     controls = controls) 
    picam2.configure(preview_config)
    
    GPIO.output(led, GPIO.HIGH) 
    picam2.start() 
    time.sleep(2)
    #Capture image in unpacked RAW format 12bit dynamic range (16bit array)
    raw = picam2.capture_array("raw").view(dtype="uint16")
    GPIO.output(led, GPIO.LOW) 
    print(picam2.capture_metadata())
    picam2.stop_preview()
    picam2.stop()

    print("Make Histogram to see Pixel Values")

    # Capture single RAW image WIthotut UV LED on
def capture_raw_background(exposure, iso):
    global raw
    # Set camera controls
    controls = {"ExposureTime": exposure, #microseconds
            "AnalogueGain": iso, # 1 = ISO 100
            "AeEnable": False, # Auto exposure and Gain
            "AwbEnable": False,# Auto white Balance
            "FrameDurationLimits": (114,239000000)} #Min/Max frame duration
    # Setup config parameters
    preview_config = picam2.create_preview_configuration(raw={"size": picam2.sensor_resolution, "format": "SBGGR12",},
                                                     controls = controls) 
    picam2.configure(preview_config)
    
    picam2.start() 
    time.sleep(2)
    #Capture image in unpacked RAW format 12bit dynamic range (16bit array)
    raw = picam2.capture_array("raw").view(dtype="uint16")
    print(picam2.capture_metadata())
    picam2.stop_preview()
    picam2.stop()
    
    print("Make Histogram to see Pixel Values")

#Display Histogram and pixel information of previous image

def display_histogram():
    
    #Get color channels in bayer order (BGGR)
    red = raw[1::2,1::2]
    green1 = raw[0::2,1::2]
    green2 = raw[1::2,0::2]
    green = np.add(green1,green2)/2
    blue = raw[0::2,0::2]
    #Make histogram for red and green channel # Set camera controls to have good pixel saturation
    Colors=("red","green","blue")
    Channel_ids=(red,green,blue)
    #Calculate the minimum and maximum value of the dataset
    min_value_red = np.min(red)
    min_value_green = np.min(green)
    min_value_blue = np.min(blue)
    max_value_red = np.max(red)
    max_value_green = np.max(green) 
    max_value_blue = np.max(blue)
    min_value = min(min_value_red, min_value_green, min_value_blue)
    max_value = max(max_value_red, max_value_green, max_value_blue)
    for channel_id, c in zip(Channel_ids,Colors):
        histogram, bin_edges=np.histogram(channel_id,bins=4095, range=(min_value,max_value))
        plt.plot(bin_edges[0:-1], histogram, color=c, linewidth = 1)
    plt.title("Red_Green histogram")
    plt.xlabel("Pixel intensity")
    plt.ylabel("Pixel Frequency")

#Get mean of pixel intensities for each channel
    mean_red = np.mean(red)
    mean_green = np.mean(green)
    mean_blue = np.mean(blue)
    
    num_red_pixels = np.count_nonzero(red)
    num_green_pixels = np.count_nonzero(green)
    num_blue_pixels =np.count_nonzero(blue)

    #print("Mean value of red:", mean_red)
    #print("Mean value of green:", mean_green)
    #print("Mean value of blue:", mean_blue)
    
    #print("Max value of red:", max_value_red)
    #print("Max value of green:", max_value_green)
    #print("Max value of blue", max_value_blue)
    
    #print("Number of red pixels:", num_red_pixels)
    #print("Number of green pixels:", num_green_pixels)
    #print("Number of blue pixels:", num_blue_pixels)

    # Add annotations to the plot
    plt.text(0.7, 0.9, f"Mean Red: {mean_red:.2f}\nMax Red: {max_value_red:.2f}\nNum Red Pixels: {num_red_pixels:.2f}", transform=plt.gca().transAxes, color='red')
    plt.text(0.7, 0.75, f"Mean Green: {mean_green}\nMax Green: {max_value_green}\nNum Green Pixels: {num_green_pixels}", transform=plt.gca().transAxes, color='green')
    plt.text(0.7, 0.55, f"Mean Blue: {mean_blue}\nMAx Blue {max_value_blue}\nNum Blue Pixels: {num_blue_pixels}", transform=plt.gca().transAxes, color='blue')

    # Save the histogram figure to the desktop
    with matplotlib.rc_context({'backend': 'Agg'}):
        desktop_path = "/home/martinoptode/Desktop/"
        filename = "histogram_figure.png"
        plt.savefig(os.path.join(desktop_path, filename))
        plt.close()  # Close the figure to release resources
    
    print("Histogrm saved to desktop")

    # Initialize lists to store column-wise means and stds for the red/green ratio
    mean_red_green_ratio_per_column = []
    std_red_green_ratio_per_column = []
    
    # Calculate the mean and std of the ratio for each column
    ratio = red / green
    mean_ratio_per_column = np.mean(ratio, axis=0)  # Average across rows for each column
    std_ratio_per_column = np.std(ratio, axis=0)    # Standard deviation across rows for each column    
    mean_red_green_ratio_per_column.append(mean_ratio_per_column)
    std_red_green_ratio_per_column.append(std_ratio_per_column)

    # Plot the mean ratio per column
    plt.plot(mean_ratio_per_column)
    plt.xlabel('Column Index')
    plt.ylabel('Mean Red/Green Ratio')
    plt.title('Mean Red/Green Ratio per Column Across All Images')

    filename = "mean_ratio_across_image_columns.png"
    plt.savefig(os.path.join(desktop_path, filename))
    plt.close()  # Close the figure to release resources
    print("Mean Red/Green Ratio plot saved to desktop")

#Capture multiple images for calibration
def capture_calibration(o2, num_images, exposure, iso, delay):
    global raw_crop
    # Set camera controls
    controls = {"ExposureTime": exposure, #microseconds
            "AnalogueGain": iso, # 1 = ISO 100
            "AeEnable": False, # Auto exposure and Gain
            "AwbEnable": False,# Auto white Balance
            "FrameDurationLimits": (114,239000000)} #Min/Max frame duration
    # Setup config parameters
    preview_config = picam2.create_preview_configuration(raw={"size": picam2.sensor_resolution, "format": "SBGGR12",},
                                                     controls = controls)
    picam2.configure(preview_config)
    
    
    for i in range(num_images):
        GPIO.output(led, GPIO.HIGH) # Turn on LED

        picam2.start() # Start Camera
        time.sleep(2)

        #Capture image in unpacked RAW format 12bit dynamic range (16bit array)
        raw = picam2.capture_array("raw").view(np.uint16)

        GPIO.output(led, GPIO.LOW) # Turn off LED

        print(picam2.capture_metadata())

        picam2.stop_preview()
        picam2.stop()

        raw_crop = raw[0:3040, 0:4056] # Remove padding from each row of pixels

        base_filename = "RAW"
        save_dir = '/home/martinoptode/Desktop/Calibration_Images/'

        # Create a new folder with date stamp if it does not exist
        date_str = datetime.now().strftime("%Y-%m-%d")
        save_dir = os.path.join(save_dir, f'{base_filename}_{date_str}')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Construct the filename with the user-defined suffix
        #filename = f'{base_filename}_{date_str}_air_sat_{suffix}.tiff'

        # Check if the filename with the user-defined suffix already exists in the folder
        count = 1
        filename = f'{base_filename}_{date_str}_{count}_air_sat{o2}.tiff'
        while os.path.exists(os.path.join(save_dir, filename)):
        # If the filename exists, add a number to the suffix and try again
            filename = f'{base_filename}_{date_str}_{count}_air_sat{o2}.tiff'
            count += 1
            # Save the image with the updated filename
        tifffile.imwrite(os.path.join(save_dir, filename), raw_crop)

        time.sleep(delay)


def capture_measurements(exposure, iso, seq_num):
    global raw
    # Set camera controls
    controls = {"ExposureTime": exposure, #microseconds
            "AnalogueGain": iso, # 1 = ISO 100
            "AeEnable": False, # Auto exposure and Gain
            "AwbEnable": False,# Auto white Balance
            "FrameDurationLimits": (114,239000000)} #Min/Max frame duration
    # Setup config parameters
    preview_config = picam2.create_preview_configuration(raw={"size": picam2.sensor_resolution, "format": "SBGGR12",},
                                                     controls = controls) 
    picam2.configure(preview_config)
    
    GPIO.output(led, GPIO.HIGH) 
    picam2.start() 
    time.sleep(2)
    #Capture image in unpacked RAW format 12bit dynamic range (16bit array)
    raw = picam2.capture_array("raw").view(dtype="uint16")
    GPIO.output(led, GPIO.LOW) 
    print(picam2.capture_metadata())
    picam2.stop()
    raw_crop = raw[0:3040, 0:4056] # Remove padding from each row of pixels

    base_filename = "RAW"
    save_dir = '/home/martinoptode/Desktop/Measurement_Images/'
    # Create a new folder with date stamp if it does not exist
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_dir = os.path.join(save_dir, f'{base_filename}_{date_str}')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # Check if the filename with the user-defined suffix already exists in the folder
    count = 1
    filename = f'{base_filename}_{date_str}_{count}_seq_num{seq_num}.tiff'
    while os.path.exists(os.path.join(save_dir, filename)):
        # If the filename exists, add a number to the suffix and try again
        filename = f'{base_filename}_{date_str}_{count}_seq_num{seq_num}.tiff'
        count += 1
        # Save the image with the updated filename
    tifffile.imwrite(os.path.join(save_dir, filename), raw_crop) 
              
   
            














    
    
    
    
 
