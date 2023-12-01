# a = 10
# b = a
# c = [1,2,3]
# d = c
# print("memory reference: ")
# print("a: ", id(a))

import webbrowser
url = 'https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox'
webbrowser.get()
webbrowser.open(url)

import socket
ip = socket.gethostbyname('www.google.com')
print(ip)