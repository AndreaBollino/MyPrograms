""" import multiprocessing


def producer(queue):
    for i in range(10):
        queue.put(i)
    queue.put(None)


def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(item)


if __name__ == '__main__':
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=producer, args=(q,))
    p2 = multiprocessing.Process(target=consumer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join() """


""" import threading
import time

def my_function():
    for i in range(5):
        print("Thread executing", i)
        time.sleep(1)

if __name__ == '__main__':
    t1 = threading.Thread(target=my_function)
    t2 = threading.Thread(target=my_function)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Program completed") """

import multiprocessing
import time

def my_function():
    for i in range(5):
        print("Process executing", i)
        time.sleep(1)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=my_function)
    p2 = multiprocessing.Process(target=my_function)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Program completed")