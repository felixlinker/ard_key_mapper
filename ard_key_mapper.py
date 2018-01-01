import json
import threading
import sys
import serial
import keyboard

def load_settings_json(filepointer):
    settings = json.load(filepointer)
    down_map = dict()
    up_map = dict()
    for _, entry in settings['key_map'].items():
        try:
            event = entry['down']
            m = down_map
        except KeyError:
            event = entry['up']
            m = up_map

        map_key = (int(event['ctrl'], 2), event['status_code'])
        m[map_key] = entry['send']

    return (settings['serial_port'], down_map, up_map)

def handle_serial_input(serial_port, down_map, up_map):
    """Reads the serial input of the arduino and sends out keystrokes accordingly"""
    ser = serial.Serial(serial_port)
    ctrl = 0
    while True:
        flag = ser.read()[0]
        value = ser.read()[0]

        if flag & 2:  # handle control button changes
            ctrl = value
        if flag & 1:  # handle press
            if (ctrl, value) in down_map:
                keyboard.press_and_release(down_map[(ctrl, value)])
        elif not flag:  # handle release
            if (ctrl, value) in up_map:
                keyboard.press_and_release(up_map[(ctrl, value)])

if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf8') as settings_fp:
        handle_arguments = load_settings_json(settings_fp)
        threading.Thread(target=handle_serial_input, daemon=True, args=handle_arguments).start()

    help_str = 'If you want to exit the program enter: exit'
    print(help_str)
    cmd = input()
    while True:
        if cmd == 'exit':
            break
        cmd = input(help_str + '\n')
