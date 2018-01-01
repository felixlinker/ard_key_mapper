# ard_key_mapper

## Description

This repo provides a python script and arduino program that allows to send custom keystrokes for a USB-HID-keyboard that is connected to an arduino (no leonardo required).
It is configured via a json and the strokes are sent to your computer via a python script.
Therefore you don't need to upload a new program to your arduino when you want to change the button map.

For example, the `settings.json` in this repository maps the down press of the Q-key on a QWERTZ-layouted keyboard to the button press and release of shift+A.

## Prerequistes

1. You need an arduino and a USB host shield with a HID-keyboard connected to it.
2. You need to the have following python packages installed
    * https://github.com/boppreh/keyboard
    * https://github.com/pyserial/pyserial
3. You need to have following arduino libraries installed
    * https://github.com/felis/USB_Host_Shield_2.0

## Setting up the `settings.json`

1. Enter the correct serial port to which the arduino is connected to the json's field `serial_port`.
2. Configure your `key_map` by giving it named entries. See below for more information.

## Configuring a `key_map` entry

A `key_map` entry is composed as follows:

```json
{
    "name": {
        "event_type": {
            "ctrl": "00000000",
            "status_code": 0
        },
        "send": "shift+x",
        "delay": 0.02
    }
}
```

Field | Description
-- | --
`name` | `name` can be replaced with any string
`event_type` | `event_type` must be replaced with any of `up` or `down` specifying the kind of button press that should be handled
`ctrl` | This field holds a value for the modifier button mask as string; see bellow for further information
`status_code` | This field holds the value which key should be pressed; you can find out it's status code by loading the `watch_status_codes.ino` program onto your arduino.
`send` | This field can holds any string that conforms to [the combination argument for keyboard.send](https://github.com/boppreh/keyboard#keyboard.send) of the python keyboard package.
`delay` | This field holds a value for a delay between button press and release in seconds and is optional.

### Modifier button mask

The control characters are implemented by an 8 bit / byte bitmask.
Every bit specifies whether a specific modifier key is hold down.
The bitmask is indexed as follows: `hgfedcba`

Index | Modifier Key
-- | --
`a`/0 | left ctrl
`b`/1 | left shift
`c`/2 | left alt
`d`/3 | left cmd
`e`/4 | right ctrl
`f`/5 | right shift
`g`/6 | right alt
`h`/7 | right cmd
