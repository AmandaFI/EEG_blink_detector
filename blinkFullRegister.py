import logging
from pynput import keyboard
from time import time

def on_release(key):
    if key == keyboard.Key.up:
        logging.info(str(time()) + ',1')
        print('Piscada.')
    elif key == keyboard.Key.right:
        logging.info(str(time()) + ',2')
        print('Piscada olho direito.')
    elif key == keyboard.Key.left:
        logging.info(str(time()) + ',3')
        print('Piscada olho esquerdo.')
    elif key == keyboard.Key.space:
        logging.info(str(time()) + ',4')
        print('Olhos forçados.')
    elif key == keyboard.Key.shift:
        logging.info(str(time()) + ',5')
        print('Outra ação.')
    elif key == keyboard.Key.backspace:
        print('Ação anteriror anulada.')
        logging.info('Erro,0')
    elif key == keyboard.Key.esc:
        print('Experimento encerrado.')
        key_listener.stop()


name = input('Digite seu nome: ')
fileName = name + '_labels' + '.csv'
print('Experimento iniciado.')
print('Aperte para registrar:')
print('Seta para cima = piscada')
print('Seta para direita = piscada somente no olho direito')
print('Seta para esquerda = piscada somente no olho esquerdo')
print('Barra de espaço = forçar os olhos')
print('Shift = ')
print('Backspace = anular o último registro feito')
print('Aperte Esc para encerrar.')

file = open(fileName,'w')
file.write('blinks\n')
file.close()

logging.basicConfig(filename=fileName, level=logging.DEBUG, format='%(message)s')

with keyboard.Listener(on_release=on_release) as key_listener:
    key_listener.join()
        