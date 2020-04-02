from time import sleep
import sys

from RPi import GPIO
from RPLCD import CharLCD

from data_extractor import get_cases
from progress_bar_chars import *
from custom_chars import *

LCD_CHAR_WIDTH = 16
SLEEP_SECONDS = 7
REFRESH_INFO_SLEEP_SECONDS = 4
SECONDS_TO_REFRESH_DATA = 1500
MAX_DATA_WIDTH = 8
PROGRESS_OUTLINE = False


lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=25, pin_e=24, pins_data=[23, 17, 4, 27])


def get_stat_chars(lcd):
    lcd.create_char(0, SIGMA)
    lcd.create_char(1, UP_ARROW)

    return chr(0), chr(1)

def prepare_progress_bar_chars(lcd): 
    if PROGRESS_OUTLINE:
        lcd.create_char(0, BAR_0_5_OUTLINE)
        lcd.create_char(1, BAR_1_5_OUTLINE)
        lcd.create_char(2, BAR_2_5_OUTLINE)
        lcd.create_char(3, BAR_3_5_OUTLINE)
        lcd.create_char(4, BAR_4_5_OUTLINE)
        lcd.create_char(5, BAR_5_5_OUTLINE)
        lcd.create_char(6, BAR_END_5_OUTLINE)
    else:
        lcd.create_char(0, BAR_0_5)
        lcd.create_char(1, BAR_1_5)
        lcd.create_char(2, BAR_2_5)
        lcd.create_char(3, BAR_3_5)
        lcd.create_char(4, BAR_4_5)
        lcd.create_char(5, BAR_5_5)
        lcd.create_char(6, BAR_END_5)


lcd.clear()
lcd.write_string('Getting data...')
lcd.cursor_pos = (1,0)
print('Getting data...')
try: 
    cases = get_cases()

except AttributeError:
    print('Fetching failed.')
    lcd.write_string('Fetching failed!')
    sys.exit(1)
lcd.write_string('Done.')
lcd.cursor_pos = (1,0)
print('Done.')
lcd.cursor_pos = (0,0)
world_cases_len = len(cases["World"]["cases"])
poland_cases_len = len(cases["Poland"]["cases"])

refresh_seconds_left = SECONDS_TO_REFRESH_DATA

def number_to_progress_bar(number: float, distinct_end=True):
    percent = 100 * number
    
    # 1.25 because 16 chars with width of 5 = 80; 100/80 = 1.25
    thin_bars = int(percent // 1.25)
    char_bars = thin_bars // 5
    progress_bar = [chr(5) for _ in range(char_bars)]
    progress_bar.append(chr(thin_bars - char_bars * 5))
    for i in range(LCD_CHAR_WIDTH - len(progress_bar) - int(distinct_end)):
        progress_bar.append(chr(0))
    if distinct_end:
        progress_bar.append(chr(6))
    return ''.join(progress_bar)


while True:
    if refresh_seconds_left < 1:
        try:
            lcd.clear()
            lcd.write_string('Fetching data...')
            lcd.cursor_pos = (0,0)
            cases = get_cases()
            world_cases_len = len(cases["World"]["cases"])
            poland_cases_len = len(cases["Poland"]["cases"])
        except AttributeError:
            pass
        refresh_seconds_left = SECONDS_TO_REFRESH_DATA
    
    TOTAL_SYMBOL, NEW_SYMBOL = get_stat_chars(lcd)
    # rjust(11) because after ': ' there are only 9 char spaces left
    lcd.write_string(f'WLD {TOTAL_SYMBOL}: {cases["World"]["cases"].rjust(9)}')
    lcd.cursor_pos = (1,0)
    lcd.write_string(f'WLD {NEW_SYMBOL}: {cases["World"]["new"].rjust(9)}')
    lcd.cursor_pos = (0,0)

    sleep(SLEEP_SECONDS)
    refresh_seconds_left -= SLEEP_SECONDS

    # lcd.clear()
    lcd.write_string(f'POL {TOTAL_SYMBOL}: {cases["Poland"]["cases"].rjust(9)}')
    lcd.cursor_pos = (1,0)
    lcd.write_string(f'POL {NEW_SYMBOL}: {cases["Poland"]["new"].rjust(9)}')
    lcd.cursor_pos = (0,0)
    sleep(SLEEP_SECONDS)
    refresh_seconds_left -= SLEEP_SECONDS

    closed_cases_fraction = int(cases["World"]["cases"].replace(',', '')) 
    closed_cases_fraction -= int(cases["World"]["active"].replace(',', ''))
    closed_cases_fraction /= int(cases["World"]["cases"].replace(',', ''))

    lcd.write_string('Control:   {:.1%}'.format(closed_cases_fraction))
    lcd.cursor_pos = (1,0)
    prepare_progress_bar_chars(lcd)
    lcd.write_string(number_to_progress_bar(closed_cases_fraction))
    lcd.cursor_pos = (0,0)
    sleep(SLEEP_SECONDS)
    refresh_seconds_left -= SLEEP_SECONDS

    # lcd.clear()
    lcd.write_string(f'Refresh in:'.ljust(LCD_CHAR_WIDTH))
    lcd.cursor_pos = (1,0)
    for i in range(REFRESH_INFO_SLEEP_SECONDS):
        if refresh_seconds_left < 1:
            break
        minutes_left = str(refresh_seconds_left // 60).zfill(2)
        seconds_left = str(refresh_seconds_left % 60).zfill(2) 
        lcd.write_string(f'{minutes_left} min  {seconds_left} s'.ljust(LCD_CHAR_WIDTH))
        lcd.cursor_pos = (1,0)
        refresh_seconds_left -= 1
        sleep(1)
    lcd.cursor_pos = (0,0)
