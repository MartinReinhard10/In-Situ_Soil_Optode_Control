import Camera_Function as cf
import Motor_Function as mf
from time import sleep


def measurement_sequence(vert_range, horiz_range, vert_overlap, horiz_overlap, vert_direction,exposure,iso,seq_num):
    """lobal rotate_right 
    rotate_right = True"""
    
    for i in range(horiz_range):
        for j in range(vert_range-1):
            if vert_direction == True:
                sleep(2)
                cf.capture_measurements(exposure,iso,seq_num)
                sleep(2)
                mf.move_vertical_UP(vert_overlap)
            else:
                sleep(2)
                cf.capture_measurements(exposure,iso,seq_num)
                sleep(2)
                mf.move_vertical_DOWN(vert_overlap)
        sleep(2)
        cf.capture_measurements(exposure,iso,seq_num)
        vert_direction = not vert_direction
        sleep(2)
        if i != horiz_range - 1:  
            mf.rotate_LEFT(horiz_overlap)
            

    # Remove Comment out if all images should be captured horizontally first before vertical movement 
    """for i in range(vert_range):
        
        #sleep(2)
        #cf.capture_measurements(exposure,iso,seq_num)
        sleep(2)
        for j in range(horiz_range-1):
            cf.capture_measurements(exposure,iso,seq_num)
            if rotate_right == True: 
                mf.rotate_RIGHT(horiz_overlap)
                sleep(2)
            else:
                mf.rotate_LEFT(horiz_overlap)
                sleep(2)
        rotate_right = not rotate_right
        print(rotate_right)
        # Capture the last image without movement
        cf.capture_measurements(exposure,iso,seq_num)
        sleep(2)
        if i < vert_range - 1:
            print("Moving up")
            
            if vert_direction == True:
                mf.move_vertical_UP(vert_overlap)
            else:
                mf.move_vertical_DOWN(vert_overlap) 
        else:
            print("No movement")"""
         
           
        

def move_to_initial_position(vert_range, horiz_range, vert_overlap, vert_direction, horiz_overlap):
    
    if vert_direction == False and horiz_range != 0:
        mf.rotate_RIGHT((horiz_range-1)*horiz_overlap)
    else:
        mf.move_vertical_DOWN((vert_range-1)*vert_overlap)
        mf.rotate_RIGHT((horiz_range-1)*horiz_overlap)

    # Remove comment out if all images should be captured horizontally first before vertical movement        
    """if rotate_right == False and horiz_range != 0:
        mf.rotate_LEFT((horiz_range - 1) * horiz_overlap)
    #elif rotate_right == False and horiz_range !=0:
        #mf.rotate_RIGHT((horiz_range - 1) * horiz_overlap)

    if vert_direction == True:
        print("moving down")
        mf.move_vertical_DOWN((vert_range - 1) * vert_overlap)  # Move up
    else:
        mf.move_vertical_UP((vert_range - 1) * vert_overlap)  # Move down"""

