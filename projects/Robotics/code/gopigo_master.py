import logging
import logging.handlers
import multiprocessing
import time


# configure listener
def listener_configurer():
    root = logging.getLogger('gpg')
    root.setLevel(logging.DEBUG)
    fh = logging.FileHandler('gopigo.log', mode='w')
    fh.setLevel(logging.INFO)
    fh_formatter = logging.Formatter('%(relativeCreated)d,%(name)s,%(message)s')
    fh.setFormatter(fh_formatter)
    root.addHandler(fh)


# This is the listener process top-level loop: wait for logging events
# (LogRecords) on the queue and handle them, quit when you get a None for a LogRecord.
def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys
            import traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


# The worker configuration is done at the start of the worker process run.
# Note that on Windows you can't rely on fork semantics, so each process
# will run the logging configuration code when it starts.
def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    # send all messages, for demo; no other level or filter logic applied.
    root.setLevel(logging.DEBUG)


# This is the worker process top-level loop, which just logs ten events with
# random intervening delays before terminating.
# The print messages are just so you know it's doing something!
def worker_process(queue, name, message, configurer):
    configurer(queue)
    logger = logging.getLogger(name)
    logger.info(message)


def color_printer(msg):
    try:
        import colorama
        from colorama import Fore, Style
        print(Fore.MAGENTA + msg + Style.RESET_ALL)
    except Exception as e:
        print(e)
        print(msg)


if __name__ == "__main__":
    color_printer("   _____       _____ _  _____         ____  ")
    print("  / ____|     |  __ (_)/ ____|       |___ \ ")
    color_printer(" | |  __  ___ | |__) || |  __  ___     __) |")
    print(" | | |_ |/ _ \|  ___/ | | |_ |/ _ \   |__ < ")
    color_printer(" | |__| | (_) | |   | | |__| | (_) |  ___) |")
    print("  \_____|\___/|_|   |_|\_____|\___/  |____/ ")
    print("                                            ")
    color_printer('\nWELCOME TO THE CREW 4 GoPiGo SCAVENGER HUNT CODE')

    # imports
    from listen_starter import *
    from drive_detect import *
    from convert2spect import convert_master
    from listen_working import listen_working
    from robo_client import connection

    # create queue for multiprocessing jobs
    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(target=listener_process,
                                       args=(queue, listener_configurer))
    listener.start()

    # listen for starting noise, code will not proceed until this executes
    recorder = Recorder()
    recorder.listen()

    # log the start sound to log file
    worker = multiprocessing.Process(target=worker_process,
                                     args=(queue, 'gpg.mic', 'Start', worker_configurer))
    worker.start()
    worker.join()

    # start gopi_master
    p2 = multiprocessing.Process(target=run_go_pi_go, args=(queue, worker_process, worker_configurer))
    p2.start()

    # start audio_detection converter
    p3 = multiprocessing.Process(target=convert_master, args=(queue, worker_process, worker_configurer))
    p3.start()

    # start audio_detection recorder
    p4 = multiprocessing.Process(target=listen_working)
    p4.start()

    # # wait until driving code is finished
    p2.join()

    # log Finish to gpg.mic
    worker = multiprocessing.Process(target=worker_process,
                                     args=(queue, 'gpg.mic', 'Finish', worker_configurer))
    worker.start()
    worker.join()

    # end log listener
    queue.put_nowait(None)
    listener.join()

    time.sleep(2)

    # send log to server
    connection('datastream.ilykei.com', 30078, 'jngallagher@uchicago.edu',
               'EyaEseaR', 19, 'gopigo.log')

    # close audio detectors
    p3.terminate()
    p4.terminate()

    # end code
    color_printer("\nSCAVENGER HUNT FINISHED!")

