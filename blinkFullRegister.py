import logging
from pynput import keyboard
from time import time

def on_release(key):
    if key == keyboard.Key.up:
        logging.info(str(time()) + ',1')
        print('Blink.')
    elif key == keyboard.Key.right:
        logging.info(str(time()) + ',2')
        print('Right eye blink.')
    elif key == keyboard.Key.left:
        logging.info(str(time()) + ',3')
        print('Left eye blink..')
    elif key == keyboard.Key.space:
        logging.info(str(time()) + ',4')
        print('Pressed eyes.')
    elif key == keyboard.Key.shift:
        logging.info(str(time()) + ',5')
        print('Other action.')
    elif key == keyboard.Key.backspace:
        print('Previous action canceled.')
        logging.info('Erro,0')
    elif key == keyboard.Key.esc:
        print('Experiment ended.')
        key_listener.stop()


name = input('Type your name: ')
fileName = name + '_labels' + '.csv'
print('Experiment started.')
print('Press to register:')
print('Up arrow = blink')
print('Right arrow = right eye blink')
print('Left arrow = light eye blink')
print('Space bar = pressed eyes')
print('Shift = ')
print('Backspace = cancel the last resgister')
print('Press Esc to end the experiment.')

file = open(fileName,'w')
file.write('blinks\n')
file.close()

logging.basicConfig(filename=fileName, level=logging.DEBUG, format='%(message)s')

with keyboard.Listener(on_release=on_release) as key_listener:
    key_listener.join()
        