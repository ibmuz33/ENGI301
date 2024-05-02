"""
--------------------------------------------------------------------------
Watch Winder Main File
--------------------------------------------------------------------------
License:   
Copyright 2023 - 2024 - Ibrahim Muzammil

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

"""

import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import busio
import adafruit_ds3231
import servo as SERVO
import button as BUTTON
import threaded_button as THREADED_BUTTON
from threading import Thread

# i2c for rtc module
i2c = busio.I2C(board.SCL_2, board.SDA_2) 
rtc = adafruit_ds3231.DS3231(i2c)
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


# setting up lcd display
lcd_columns = 16
lcd_rows = 2

# lcd display pin setup
lcd_rs        = digitalio.DigitalInOut(board.P2_6)
lcd_en        = digitalio.DigitalInOut(board.P2_4)
lcd_d4        = digitalio.DigitalInOut(board.P2_2)
lcd_d5        = digitalio.DigitalInOut(board.P2_5)
lcd_d6        = digitalio.DigitalInOut(board.P2_3)
lcd_d7        = digitalio.DigitalInOut(board.P2_1)
lcd_backlight = digitalio.DigitalInOut(board.P2_7)

# Initialise the LCD class
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)


# servo pins
servo          = SERVO.Servo("P1_36", default_position=0)


# set of threaded buttoms
buttonR         = THREADED_BUTTON.ThreadedButton("P2_35")
buttonG         = THREADED_BUTTON.ThreadedButton("P2_33")
buttonB         = THREADED_BUTTON.ThreadedButton("P2_31")
buttonY        = THREADED_BUTTON.ThreadedButton("P2_29")

#staring button classes
buttonR.start()
buttonG.start()
buttonB.start()
buttonY.start()

x = 0
while True:
    # Main loop:
      
     # welcome screen: can set time or start winding
    while x == 0:
        lcd.message = "G - Set Time\nB - Quick Start"
        if ( buttonB.get_last_press_duration() > 0.1):
            buttonB.press_duration = 0.0
            lcd.clear()
            x = 1
            break
        elif ( buttonG.get_last_press_duration() > 0.1):
            buttonG.press_duration = 0.0
            lcd.clear()
            x = 2
            break
            
    ini2 = 0
    # winding screen
    while x == 1:
        servoRun = 1;
        if ini2 == 0:
            sleep = 2
            lcd.backlight = True
            speed = "3"
            dndStatus = "off"
            ledStatus = "on"
            # ability to go back to welcome screen and stop winding
        if ( buttonR.get_last_press_duration() > 0.1):
            buttonR.press_duration = 0.0
            ini2 = 0
            x=0
            lcd.clear()
            servoRun = 0;
            break
        # Button not needed
        elif ( buttonG.get_last_press_duration() > 0.1):
            buttonG.press_duration = 0.0
            pass
        # turn on or off Do not Disturb
        elif ( buttonB.get_last_press_duration() > 0.1):
            buttonB.press_duration = 0.0
            ini2 = 1
            if dndStatus == "off":
                dndStatus = "on"
            else:
                dndStatus = "off"
            lcd.clear()
        # Turn LCD backlight on or off
        elif (buttonY.get_last_press_duration() > 0.1):
            ini2 = 1
            buttonY.press_duration = 0.0
            if ledStatus == "on":
                ledStatus = "off"
                lcd.backlight = False
            else:
                ledStatus = "on"
                lcd.backlight = True
            lcd.clear()
        topString = ("B:DND-"+dndStatus)
        botString = "R:<- "+"Y:BKLT-"+ledStatus
        lcd.message = topString+"\n"+botString
        t = rtc.datetime
        #turning servo based on do not disturb
        if dndStatus == "on":
            if (t.tm_hour < 8 or t.tm_hour > 20):
                pass
            else:
                servo.turn(0)
                time.sleep(2)
                servo.turn(100)
                time.sleep(2)
        else:
                servo.turn(0)
                time.sleep(2)
                servo.turn(100)
                time.sleep(2)
            
    # ability to set time
    ini = 0    
    while x == 2:
        if ini == 0:
            hr = 6
            amPm = " AM"
            #+1 or -1 hours
        if ( buttonR.get_last_press_duration() > 0.1):
            buttonR.press_duration = 0.0
            ini = 1
            hr = hr+1
            if hr == 13:
                hr = 1
            lcd.clear()
        elif ( buttonG.get_last_press_duration() > 0.1):
            buttonG.press_duration = 0.0
            ini = 1
            hr = hr-1
            if hr == 0:
                hr = 12
            lcd.clear()
            #change from am to pm
        elif ( buttonB.get_last_press_duration() > 0.1):
            buttonB.press_duration = 0.0
            ini = 1
            if amPm == " AM":
                amPm = " PM"
            else:
                amPm = " AM"
            lcd.clear()
            # go back to welcome screen
        elif (buttonY.get_last_press_duration() > 0.1):
            buttonY.press_duration = 0.0
            if amPm == " PM":
                hr = hr+12
            t = time.struct_time((2017, 10, 29, hr, 14, 15, 0, -1, -1))
            rtc.datetime = t
            ini=0
            lcd.clear()
            x=0
            break
        topString = ("Time : "+str(hr)+amPm)
        botString = "R+1 G-1 B:AP Y->"
        lcd.message = topString+"\n"+botString