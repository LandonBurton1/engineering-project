############################################################
#################### IMPORT LIBRARIES ######################
############################################################
from time import sleep                     # <<< DO NOT MODIFY >>>
sleep(5) # required for stability          # <<< DO NOT MODIFY >>>

# Imports for MQTT communication           # <<< DO NOT MODIFY >>>
import network                             # <<< DO NOT MODIFY >>>
import json                                # <<< DO NOT MODIFY >>>
from umqtt.robust import MQTTClient        # <<< DO NOT MODIFY >>>

# Imports the library to make a random number. This is used to
#    create a psuedo temperature value to transmit for demo
#    purposes. You don't need this library for the project.
import random
from picozero import RGBLED, Button
from math import log
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import random
############################################################
################# SPECIFY PINS AND OBJECTS #################
############################################################
relaysig =  Pin(17, Pin.OUT)
display_width = 128 # pixel x values = 0 to 127
display_height = 64 # pixel y values = 0 to 63
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) # TX pin is Pin 0, RX pin is Pin
display = SSD1306_I2C(display_width, display_height, i2c)
button = Button(14)
led = RGBLED(10,11,12)
therm =ADC(28)
pot = ADC(26)


############################################################
##################### OTHER SETUP STUFF ####################
############################################################

#steinhart constants

A= 1.129e-3
B = 2.341e-4
C = 8.767e-8

#variables
v_in = 3.3 #volts
R1 = 10000 #ohms




# Wi-Fi and MQTT settings
SSID = "WilfongEngr301" # Raspberry Pi 4 Wi-Fi name                               # <<< DO NOT MODIFY >>>
PASSWORD = "BoilerUp" # Raspberry Pi 4 Wi-Fi password, WPA/WPA2 security          # <<< DO NOT MODIFY >>>
MQTT_BROKER = "10.42.0.1"  # Raspberry Pi 4's IP                                  # <<< DO NOT MODIFY >>>
TOPIC = "pico/data" # "pico/data" is just a label                                 # <<< DO NOT MODIFY >>>
                    # It helps organize messages, like folders in a file system.  # <<< DO NOT MODIFY >>>
                    # The TOPIC could be any string, but leave it as "pico/data"  # <<< DO NOT MODIFY >>>

SENSOR_ID = "Team03"  # !!!-- CHANGE THIS AS DIRECTED BY DR. WILFONG --!!!

# Connect to Wi-Fi                                          # <<< DO NOT MODIFY >>>
wlan = network.WLAN(network.STA_IF)                         # <<< DO NOT MODIFY >>>
wlan.active(True)                                           # <<< DO NOT MODIFY >>>
wlan.config(pm = 0xa11140) # disable Wi-Fi low power mode   # <<< DO NOT MODIFY >>>
wlan.connect(SSID, PASSWORD)                                # <<< DO NOT MODIFY >>>

print("Attempting to connect to Wi-Fi")
while not wlan.isconnected():                               # <<< DO NOT MODIFY >>>
    pass                                                    # <<< DO NOT MODIFY >>>

sleep(2)  # Extra delay for stability                       # <<< DO NOT MODIFY >>>
print("Connected to Wi-Fi!")



# Connect to MQTT broker with reconnect support         # <<< DO NOT MODIFY >>>
client = MQTTClient(f"client_{SENSOR_ID}", MQTT_BROKER) # <<< DO NOT MODIFY >>>
client.DEBUG = True                                     # <<< DO NOT MODIFY >>>

# Try to connect to MQTT broker                         # <<< DO NOT MODIFY >>>
try:                                                    # <<< DO NOT MODIFY >>>
    client.connect()                                    # <<< DO NOT MODIFY >>>
    print("Connected to MQTT broker!")
    display.fill(0) # clears display
    display.text("Connected.", 0, 0) # write text starting at x=0 and y=0
    display.show() # make the changes take effect
except Exception as e:                                  # <<< DO NOT MODIFY >>>
    print("Failed to connect to MQTT broker:", e)
    display.fill(0) # clears display
    display.text("Failed to connect.", 0, 0) # write text starting at x=0 and y=0
    display.show() # make the changes take effect
    
    
############################################################
#########FUNCTIONS #########################################
def getTempC():
    adc_value = therm.read_u16() #value of 65535 
    V_out = (v_in/65535) * adc_value
    Rt = (V_out * R1) / (v_in - V_out)
    Tempk = 1/(A +(B*log(Rt)) + (C * pow(log(Rt),3))) # Converting the ADC val to Kelvin using steinhart
    TempC = Tempk - 273.15 #Changing from Kelvin to Celsius
    

    return(TempC)
def getTempF():
    adc_value = therm.read_u16() #value of 65535 
    V_out = (v_in/65535) * adc_value
    Rt = (V_out * R1) / (v_in - V_out)
    Tempk = 1/(A +(B*log(Rt)) + (C * pow(log(Rt),3))) # Converting the ADC val to Kelvin using steinhart
    TempC = Tempk - 273.15 #Changing from Kelvin to Celsius
    TempF = TempC * (9/5) + 32 #Celsius to Farenheit

    return(TempF)
def getTempK():
    adc_value = therm.read_u16() #value of 65535 
    V_out = (v_in/65535) * adc_value
    Rt = (V_out * R1) / (v_in - V_out)
    Tempk = 1/(A +(B*log(Rt)) + (C * pow(log(Rt),3))) # Converting the ADC val to Kelvin using steinhart
    return(Tempk)


###########
### global variables ####
Relstate = 0 # Relay on or off
VTemp = ((26/65535) * 65535)+ 


########
### Lock code

flag = False
while flag == False:
    
    
    
    flag = True

sleep(3)
############################################################
####################### INFINITE LOOP ######################
############################################################

x = 0
base = 19
old = button.is_pressed #true or false
while True: 
    if getTempC() >= base - VTemp and getTempC() <=base + VTemp:
        led = (0,255,0)
    else:
        led = (255,0,0)
        led.toggle()
    temperature_sensor_reading = getTempC()
    if x == 0:
        temperature_sensor_reading = getTempC()
        x = x+1
        display.fill(0) # clears display
        display.text("Celcius: ", 0, 0) # write text starting at x=0 and y=0
        display.text(str(getTempC()), 0, 10) # write text starting at x=0 and y=0
        display.text("Press to change", 0, 50) # write text starting at x=0 and y=0
        display.show() # make the changes take effect
    new = button.is_pressed 
    if(old == True and new == False):
        print("Button Pressed")
        if x ==1:
            x = x+1
            display.fill(0) # clears display
            display.text("Fahrenheit: ", 0, 0) # write text starting at x=0 and y=0
            display.text(str(getTempF()), 0, 10) # write text starting at x=0 and y=0
            display.text("Press to change", 0, 50) # write text starting at x=0 and y=0
            display.show() # make the changes take effect
        elif x==2:
            x = 0
            display.fill(0) # clears display
            display.text("Kelvin: ", 0, 0) # write text starting at x=0 and y=0
            display.text(str(getTempK()), 0, 10) # write text starting at x=0 and y=0
            display.text("Press to change", 0, 50) # write text starting at x=0 and y=0
            display.show() # make the changes take effect
    old = new
    
    
    
    # Create and send MQTT payload                               # <<< DO NOT MODIFY >>>
    message_data = {                                             # <<< DO NOT MODIFY >>>
        "sensorID": SENSOR_ID,                                   # <<< DO NOT MODIFY >>>
        "temperatureReading": temperature_sensor_reading         # <<< DO NOT MODIFY >>>
    }                                                            # <<< DO NOT MODIFY >>>
    message_json = json.dumps(message_data)  # Convert to JSON   # <<< DO NOT MODIFY >>>
    
    # Try to publish message to MQTT broker                                    # <<< DO NOT MODIFY >>>
    try:                                                                       # <<< DO NOT MODIFY >>>
        client.publish(TOPIC, message_json, retain=True) # Send MQTT payload   # <<< DO NOT MODIFY >>>
        print(f"Published: {message_json}") # Print MQTT payload to the Shell
    except Exception as e:                                                     # <<< DO NOT MODIFY >>>
        print("Publish failed:",e)
    
    sleep(2) # Send MQTT payload every 2 seconds