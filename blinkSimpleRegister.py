import logging
from pynput.mouse import Listener, Button
from time import time

def on_click(x,y, button,pressed):
    if pressed and button == Button.left:
        logging.info(str(time()) + ',1')
        print('Piscada registrada.')
    elif pressed and button == Button.right:
        logging.info('Erro,0')
        print('Piscada anterior anulada.')

def on_scroll(x,y,dx,dy):
    listener.stop()
    print('Experimento encerrado.')

name = input('Digite seu nome: ')
fileName = name + '_labels' + '.csv'
print('Experimento iniciado.')
print('Aperte o botão esquerdo do mouse para registrar uma piscada e o botão direito para anular a última piscada registrada.')
print('Role o scroll do mouse para encerrar.')

file = open(fileName,'w')
file.write('blinks\n')
file.close()

logging.basicConfig(filename=fileName, level=logging.DEBUG, format='%(message)s')

with Listener(on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()