from Raspi_PWM_Servo_Driver import PWM
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

# Create instance for I2C communication
i2c = busio.I2C(board.SCL, board.SDA)

# Create instance for ADC board
ads = ADS.ADS1115(i2c)

# Create variables for each analog port in use
x = AnalogIn(ads, ADS.P0)
y = AnalogIn(ads, ADS.P1)

# Write down ADC min and max values
ADC_min = 0
ADC_max = 32767

# Create instance and initilize the PWM device (the motorhat)
pwm = PWM(0x6F)

# Set Servo minimum and maximum pulse length values (out of 4096)
servoMin = 150
servoMax = 600
servoMid = (servoMin + servoMax)//2 

# Set PWM frequency for servos
pwm.setPWMFreq(60)

# Name each channel to keep track of which is which (use the channel numbers on the motor hat)
x_axis = 1
y_axis = 0

# Function to replicate the Arduino "map()" function
def arduino_map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Start main program with try/except to make use of keyboard interrupt
try:
    # Let the user know the program is starting
    print("Starting program.")

    # Set the servos the centered position so they know how it looks like
    print("Setting servos to center position for reference.")
    pwm.setPWM(x_axis, 0, servoMid)
    pwm.setPWM(y_axis, 0, servoMid)

    # Pause the program so that the user has time to notive
    time.sleep(3)

    # Let the user know that the knob position needs to be centered or else the servos will not be centered.
    print("Set knobs to center position to keep servos centered.")

    # The main program loop will now begin
    print("Ready for user control.")

    # Loop that will keep control the servos according to user input on the knobs
    while True:
        # Set ADC values in static variable so we are able to filter out the negatives that the ADC produces
        x_pot = x.value
        y_pot = y.value

        # Ensure that the negative values from ADC are not used
        if x_pot >= 0 and y_pot >= 0 and x_pot <= 32767 and y_pot <= 32767:
            # Map the potentiometer value to the servo control values
            # Note: servoMax & servoMin are flipped so that the knob orientation makes sense to the user
            position_x = arduino_map(x_pot, ADC_min, ADC_max, servoMax, servoMin)
            position_y = arduino_map(y_pot, ADC_min, ADC_max, servoMax, servoMin)

            # Print out the ADC values for debugging purposes
            print("ADC values (x,y):"+str(x_pot)+","+str(y_pot))

            # Print out the mapped servo values for debugging and for user viewing
            print("Position in x-axis:"+str(position_x)+" Position in y-axis:"+str(position_y))

            # Send the mapped servo values to the motor hat
            pwm.setPWM(x_axis, 0, position_x)
            pwm.setPWM(y_axis, 0, position_y)

        # if the ADC bit value is negative, loop again until the value is no longer negative
        else:
            continue

# End the program once it detects a user action
except KeyboardInterrupt:
    print("Detected user interrupt.")
    print("Ending program.")
