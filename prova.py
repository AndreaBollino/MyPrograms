""" def hello():
    print('Ueeee')

hello()


def getAnswer(number):
    if number == 1:
        return 'sicuro'

fortuna=getAnswer(1)
print(fortuna)
 """
# class Dog:
#     def __init__(self, name, breed):
#         self.name = name
#         self.breed = breed
#     def bark(self):
#         print("Woof!")

# my_dog = Dog("Fido", "Golden Retriever")
# print(my_dog.name) # "Fido"
# my_dog.bark() # "Woof!"

# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# @my_decorator
# def say_whee():
#     print("Whee!")

# say_whee()

# generator function
""" def my_gen():
    n = 1
    print('This is printed first')
    yield n

    n += 1
    print('This is printed second')
    yield n

    n += 1
    print('This is printed at last')
    yield n

# using for loop
for item in my_gen():
    print(item) """

# import threading
# import time

# def worker():
#     time.sleep(5)
#     print(str(threading.get_ident())+"\n")
#     #print(n)
#     #time.spleep(10/i)
#     #secondi=10/n
    

# threads = []
# for i in range(5):
#     t = threading.Thread(target=worker)
#     threads.append(t)
#     t.start() 

# """ import threading

# def worker():
#     print(threading.get_ident())

# threads = []
# for i in range(5):
#     t = threading.Thread(target=worker)
#     #threads.append(t)
#     t.start() """

try:
    x = 1 / 0
except ZeroDivisionError as e:
    print("Error Code:", e)