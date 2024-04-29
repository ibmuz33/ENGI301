import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import busio
import adafruit_ds3231
import servo as SERVO
import button as BUTTON

# i2c = board.I2C()  # uses board.SCL and board.SDA
i2c = busio.I2C(board.SCL_2, board.SDA_2) 
rtc = adafruit_ds3231.DS3231(i2c)
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


lcd_columns = 16
lcd_rows = 2

# BeagleBone Black configuration:
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


servo          = SERVO.Servo("P1_36", default_position=100)
SERVO_LOCK         = 100     # Fully anti-clockwise
SERVO_UNLOCK       = 0       # Fully clockwise

buttonR="P1_36"
buttonG="P1_34"
buttonB="P1_32"
buttonY="P1_30"

# pylint: disable-msg=using-constant-test
if False:  # change to True if you want to set the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2017, 10, 29, 15, 14, 15, 0, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)  # uncomment for debugging
    rtc.datetime = t
    print()
# pylint: enable-msg=using-constant-test

# Main loop:
while True:
    t = rtc.datetime
    # print(t)     # uncomment for debugging
    print(
        "The date is {} {}/{}/{}".format(
            days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
        )
    )
    print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
    lcd.backlight = True
    # Print a two line message
    lcd.message = "time {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec)
    lcd.cursor = True
    lcd.blink = True
    lcd.cursor_position(0, 0)
    # Wait 5s
    servo.turn(0)
    time.sleep(5)
    servo.turn(100)
    time.sleep(5)
    lcd.clear()
    