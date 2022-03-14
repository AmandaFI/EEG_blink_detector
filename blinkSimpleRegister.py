import logging
from pynput.mouse import Listener, Button
from time import time

def on_click(x,y, button,pressed):
    if pressed and button == Button.left:
        logging.info(str(time()) + ',1')
        print('Blink registered.')
    elif pressed and button == Button.right:
        logging.info('Erro,0')
        print('Previous blink canceled.')

def on_scroll(x,y,dx,dy):
    listener.stop()
    print('Experiment ended.')

name = input('Type your name: ')
fileName = name + '_labels' + '.csv'
print('Experiment started.')
print('Press the left mouse button to register a blink and the right mouse button to cancel the last blink registered.')
print('Scroll the mouse to end the experiment.')

file = open(fileName,'w')
file.write('blinks\n')
file.close()

logging.basicConfig(filename=fileName, level=logging.DEBUG, format='%(message)s')

with Listener(on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()