import threading
from time import sleep

quit_event = threading.Event()
print_lock = threading.Lock()


def safe_print(msg):
    with print_lock:
        print(msg)
#end safe_print

def quitter():
    while True:
        vin = input("q to quit: ")

        if vin.strip().lower() == "q":
            safe_print("Stopping...")
            quit_event.set()
            break
#end quitter

def worker():
    while not quit_event.is_set():
        safe_print("in worker")
        sleep(0.5)
    safe_print("worker exiting")
#end worker
    
t1 = threading.Thread(target=quitter)
t2 = threading.Thread(target=worker)

t1.start()
t2.start()

t1.join()
t2.join()

print("program ended")