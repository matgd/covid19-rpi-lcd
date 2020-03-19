from time import sleep

from RPi import GPIO
from RPLCD import CharLCD

from data_extractor import get_cases


SLEEP_SECONDS = 7
SECONDS_TO_REFRESH_DATA = 1200
MAX_DATA_WIDTH = 8

lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=25, pin_e=24, pins_data=[23, 17, 4, 27])

print('Getting data...')
cases = get_cases()
print('Done.')
world_cases_len = len(cases["World"]["cases"])
poland_cases_len = len(cases["Poland"]["cases"])
refresh_seconds_left = SECONDS_TO_REFRESH_DATA

while True:
    if refresh_seconds_left < 0:
        cases = get_cases()
        world_cases_len = len(cases["World"]["cases"])
        poland_cases_len = len(cases["Poland"]["cases"])
    lcd.clear()
    lcd.write_string(f'WLD ALL:{cases["World"]["cases"].rjust(MAX_DATA_WIDTH)}')
    lcd.cursor_pos = (1, 0)
    wld_new_string = ("+" + cases["World"]["new"]).rjust(MAX_DATA_WIDTH)
    lcd.write_string(f'WLD NEW:{wld_new_string}')
    lcd.cursor_pos = (0, 0)

    sleep(SLEEP_SECONDS)
    refresh_seconds_left -= SLEEP_SECONDS

    lcd.clear()
    lcd.write_string(f'POL ALL:{cases["Poland"]["cases"].rjust(MAX_DATA_WIDTH)}')
    lcd.cursor_pos = (1, 0)
    lcd.write_string(f'POL NEW:{cases["Poland"]["new"].rjust(MAX_DATA_WIDTH)}')
    lcd.cursor_pos = (0, 0)
    sleep(SLEEP_SECONDS)
    refresh_seconds_left -= SLEEP_SECONDS
