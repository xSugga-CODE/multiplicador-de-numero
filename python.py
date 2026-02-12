import time
import threading
import msvcrt


def input_number():
    while True:
        try:
            s = input("ingresa un numero: ")
            if s.strip() == "":
                print("No ingresaste nada, intenta de nuevo.")
                continue
            return float(s)
        except ValueError:
            print("Eso no es un número, intenta de nuevo.")


def key_listener(pause_event, running_flag):
    print("Controles: 'p' pausa/reanuda, 'q' sale.")
    while running_flag['run']:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            try:
                key = ch.decode('utf-8').lower()
            except Exception:
                continue
            if key == 'p':
                if pause_event.is_set():
                    pause_event.clear()
                    print("Reanudado.")
                else:
                    pause_event.set()
                    print("Pausado.")
            elif key == 'q':
                running_flag['run'] = False
                print("Saliendo...")
                break
        time.sleep(0.1)


def main():
    numero = input_number()
    pause_event = threading.Event()  # cuando está seteado => pausado
    running_flag = {'run': True}
    listener = threading.Thread(target=key_listener, args=(pause_event, running_flag), daemon=True)
    listener.start()
    interval = 2.0
    try:
        while running_flag['run']:
            if not pause_event.is_set():
                numero *= 2
                print(numero)
                waited = 0.0
                step = 0.1
                while waited < interval and running_flag['run'] and not pause_event.is_set():
                    time.sleep(step)
                    waited += step
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print('\nInterrupción por teclado. Saliendo.')
    print('Programa terminado.')


if __name__ == '__main__':
    main()
