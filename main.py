"""
Keyboard control via Serial port.

Requirements: Python 3.X

Dependencies:
- pyserial
- ipdb
- pyautogui
"""

import time

import pyautogui
from serial import Serial
from serial.tools import list_ports

from logger import get_logger


logger = get_logger()

SERIAL_DEVICE_NAME = '/dev/cu.usbmodem1411'

PRESS_ACTION_TYPE = 'press'
HOTKEY_ACTION_TYPE = 'hotkey'

YOUTUBE_ACTIONS = {
    'play_pause': {
        'shortcut': ['space'],
        'type': PRESS_ACTION_TYPE,
    },
    'rewind': {
        'shortcut': ['left'],
        'type': PRESS_ACTION_TYPE,
    },
    'forward': {
        'shortcut': ['right'],
        'type': PRESS_ACTION_TYPE,
    },
    'volume_up': {
        'shortcut': ['shift','up'],
        'type': HOTKEY_ACTION_TYPE,
    },
    'volume_down': {
        'shortcut': ['shift','down'],
        'type': HOTKEY_ACTION_TYPE,
    },
    'mute_unmute': {
        'shortcut': ['m'],
        'type': PRESS_ACTION_TYPE,
    },
    'fullscreen': {
        'shortcut': ['f'],
        'type': PRESS_ACTION_TYPE,
    },
    'escape': {
        'shortcut': ['esc'],
        'type': PRESS_ACTION_TYPE,
    },
    'captions': {
        'shortcut': ['c'],
        'type': PRESS_ACTION_TYPE,
    },
}

def keyboard_control(action):
    """
    Keyboard keys:
    https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
    """
    action_selected = YOUTUBE_ACTIONS.get(str(action))
    logger.info("action: {}".format(action))
    if action_selected:
        if action_selected['type'] == PRESS_ACTION_TYPE:
            pyautogui.press(*action_selected['shortcut'])
        elif action_selected['type'] == HOTKEY_ACTION_TYPE::
            pyautogui.hotkey(*action_selected['shortcut'])
    else:
        logger.warning("Action not found.")

def demo_controls():
    """Short demo from all actions"""
    for k,_ in YOUTUBE_ACTIONS.items():
        time.sleep(2)
        keyboard_control(k)


def read_serial(port, baudrate=9600):
    """
    Open a serial connection.

    Doc: https://pyserial.readthedocs.io/en/latest/pyserial_api.html

    Args:
    - port: (string|required) Device name
    - baudrate: (int|required) Baud rate such as 9600 or 115200 etc.

    """
    # Setup
    arduino_comm = Serial()
    arduino_comm.port = port
    arduino_comm.baudrate = baudrate

    try:
        arduino_comm.open()
        logger.info("Serial port opened: {port} - Baud rate: {baudrate} bits/second".format(
            port=port,
            baudrate=baudrate,
        ))
    except Exception as e:
        logger.error("Error open serial port: {}".format(e))

    if arduino_comm.isOpen():
        try:
            while True:
                message = arduino_comm.readline().decode("utf-8").rstrip()
                logger.info("Msg received: {}".format(message))
                keyboard_control(action=message)
        except Exception as e1:
            logger.error("Error communicating: {}".format(e1))
        except KeyboardInterrupt:
            logger.info("Exit.")
        finally:
            arduino_comm.close()
            logger.info("Device closed")
    else:
        logger.error("Cannot open serial port")


def serial_ports():
    """ Lists serial port names.
    In addition, show all ports available in console.

    returns:
        A list of the serial ports available on the system
    """
    ports = list(list_ports.comports())
    for port in ports:
        logger.info(port.__dict__)
    return ports


if __name__ == "__main__":
    read_serial(SERIAL_DEVICE_NAME)
