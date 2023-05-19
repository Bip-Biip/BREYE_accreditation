import time
import keyboard
from enum import Enum, auto

class State(Enum):
    RELEASED = auto()
    PRESSED = auto()
    STAND_BY = auto()

six_keys = ['f', 'd', 's', 'j', 'k', 'l']
six_states = [State.RELEASED]*6
current_sum = 0
action = print

def _on_press(key):
    global current_sum
    try:
        i = six_keys.index(key.name)
    except:
        return
    if six_states[i] != State.PRESSED:
        six_states[i] = State.PRESSED
        current_sum += pow(2, i)

def _on_release(key):
    global current_sum 
    try:
        i = six_keys.index(key.name)
    except:
        if key.name == 'space':
            action(0)
        else:
            print(f"{key.name} => {key.scan_code}")
        return
    six_states[i] = State.RELEASED
    b = True
    for s in six_states:
        b = b and s == State.RELEASED
    if b:
        action(current_sum)
        current_sum = 0

def _hook(key):
    if key.event_type == 'up':
        _on_release(key)
    else:
        _on_press(key)

keyboard.hook(_hook)
time.sleep(10)

