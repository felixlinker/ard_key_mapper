import json
import threading
import serial
import keyboard

SETTINGS = dict()
DOWN_MAP = dict()
UP_MAP = dict()
with open('./settings.json', encoding='utf8') as fp:
    SETTINGS = json.load(fp)

for _, entry in SETTINGS['key_map'].items():
    try:
        event = entry['down']
        m = DOWN_MAP
    except KeyError:
        event = entry['up']
        m = UP_MAP

    map_key = (int(event['ctrl'], 2), event['status_code'])
    m[map_key] = entry['send']

SER = serial.Serial(SETTINGS['serial_port'])

def handle_serial_input():
    """Reads the serial input of the arduino and sends out keystrokes accordingly"""
    ctrl = 0
    while True:
        flag = SER.read()[0]
        value = SER.read()[0]

        if flag & 2:  # handle control button changes
            ctrl = value
        if flag & 1:  # handle press
            if (ctrl, value) in DOWN_MAP:
                keyboard.press_and_release(DOWN_MAP[(ctrl, value)])
        elif not flag:  # handle release
            if (ctrl, value) in UP_MAP:
                keyboard.press_and_release(UP_MAP[(ctrl, value)])

if __name__ == '__main__':
    threading.Thread(target=handle_serial_input, daemon=True).start()

    help_str = 'If you want to exit the program enter: exit'
    print(help_str)
    cmd = input()
    while True:
        if cmd == 'exit':
            break
        cmd = input(help_str + '\n')
