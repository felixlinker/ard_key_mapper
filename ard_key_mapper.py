import json
import threading
import sys
import time
import serial
import keyboard

def get_default_event(default_settings={}):
    default = {
        'down': {'ctrl': '00000000', },
        'up': {'ctrl': '00000000', },
        'delay': 0,
    }
    default['down'].update(default_settings.pop('down', {}))
    default['up'].update(default_settings.pop('up', {}))
    default.update(default_settings)

    return (default, default.pop('down'), default.pop('up'))

def load_settings_json(filepointer):
    settings = json.load(filepointer)
    default_event, default_down, default_up = get_default_event(settings.get('default_event', {}))

    down_map = dict()
    up_map = dict()
    for _, org_entry in settings['key_map'].items():
        entry = default_event.copy()
        entry.update(org_entry)
        try:
            event = default_down.copy()
            event.update(entry['down'])
            m = down_map
        except KeyError:
            event = default_up.copy()
            event.update(entry['up'])
            m = up_map

        map_key = (int(event['ctrl'], 2), event['status_code'])
        m[map_key] = {
            'combination': entry['send'],
            'delay': entry['delay']
        }

    return (settings['serial_port'], down_map, up_map)

def handle_serial_input(serial_port, down_map, up_map):
    """Reads the serial input of the arduino and sends out keystrokes accordingly"""
    ser = serial.Serial(serial_port)
    ctrl = 0
    while True:
        flag = ser.read()[0]
        value = ser.read()[0]

        combination = ""
        delay = 0
        if flag & 2:  # handle control button changes
            ctrl = value
        if flag & 1:  # handle press
            if (ctrl, value) in down_map:
                combination = down_map[(ctrl, value)]['combination']
                delay = down_map[(ctrl, value)]['delay']
        elif not flag:  # handle release
            if (ctrl, value) in up_map:
                combination = up_map[(ctrl, value)]['combination']
                delay = up_map[(ctrl, value)]['delay']

        if combination:
            if delay:
                keyboard.press(combination)
                time.sleep(delay)
                keyboard.release(combination)
            else:
                keyboard.press_and_release(combination)


if __name__ == '__main__':
    settings_path = 'settings.json'
    if len(sys.argv) > 1:
        settings_path = sys.argv[1]

    with open(settings_path, encoding='utf8') as settings_fp:
        handle_arguments = load_settings_json(settings_fp)
        threading.Thread(target=handle_serial_input, daemon=True, args=handle_arguments).start()

    while True:
        cmd = input('If you want to exit the program enter: exit\n')
        if cmd == 'exit':
            break
