from os import environ as env
from gpiozero import Button
from signal import pause

button_pins = [
    'BTN_1_GPIO',
    'BTN_2_GPIO',
    'BTN_3_GPIO',
    'BTN_4_GPIO'
]

button_numbers = [
    'BTN_1_NUMBER',
    'BTN_2_NUMBER',
    'BTN_3_NUMBER',
    'BTN_4_NUMBER'
]

# Code fragment to cheat on .env loading
from dotenv import load_dotenv
load_dotenv()


# Ensure all required button definitions are set as environment variables
for BTN_GPIO in button_pins:
    try:
        env[BTN_GPIO]
        print(f'[info]: {BTN_GPIO} is defined as GPIO {env[BTN_GPIO]}')
    except KeyError:
        print(f'[error]: {BTN_GPIO} environment variable is required')

class NumberedButton(Button):
    def __init__(self, number=None, *args, **kw):
        super().__init__(*args, **kw)
        self.number = number
            

# Define buttons for all GPIO in button_pins
button_1 = NumberedButton(number=env[button_numbers[0]], pin=env[button_pins[0]], bounce_time=0.02) # 6  = GPIO6
button_2 = NumberedButton(number=env[button_numbers[1]], pin=env[button_pins[1]], bounce_time=0.02) # 13 = GPIO13
button_3 = NumberedButton(number=env[button_numbers[2]], pin=env[button_pins[2]], bounce_time=0.02) # 19 = GPIO19
button_4 = NumberedButton(number=env[button_numbers[3]], pin=env[button_pins[3]], bounce_time=0.02) # 26 = GPIO26



def pressed(button):
    print(f"Button {button.number} pressed")
    return button.number

# You can assign a callback function so the button instance is passed into the callback
button_1.when_pressed = pressed
button_2.when_pressed = pressed
button_3.when_pressed = pressed
button_4.when_pressed = pressed

# pause()