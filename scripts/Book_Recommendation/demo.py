#!/usr/bin/env python3
import numpy as np
import yaml
import speech_recognition as sr
import pyttsx3
import cv2

def init_engine():
    engine = pyttsx3.init()
    return engine

def say(s, engine):
    engine.say(s)
    engine.runAndWait()

r = sr.Recognizer()

user_list = ["alex", "public"]

with sr.Microphone() as source:
    ask_for_book = r.listen(source, 10, 3)

activate = r.recognize_google(ask_for_book, language="en-IN")
print(activate)
name1 = None
engine = init_engine()
try:
    say("ok wut is ur name?", engine)

    with sr.Microphone() as source:
        name = r.listen(source, 10, 3)
    user = r.recognize_google(name)
    name = name.lower()
    name1 = name
except:
    user = "alex"

eps = 1e-10
if name1 is not None:
    if "alex" in name1:
        user = "alex"

user_file = f'Users/{user}.yaml'
with open(user_file, 'r') as file:
    user_yaml = dict(yaml.safe_load(file))
user_read = user_yaml['read']
del user_yaml['read']
user_read = map(lambda x: x.lower(), user_read)
user_sum = sum(user_yaml.values())
user_poss = {k: v / user_sum + eps for k, v in user_yaml.items()}

public_file = 'Users/Public.yaml'
with open(public_file, 'r') as file:
    public_yaml = dict(yaml.safe_load(file))
public_sum = sum(public_yaml.values())
public_poss = {k: v / public_sum + eps for k, v in public_yaml.items()}

for k in user_poss.keys():
    user_poss[k] = (user_poss[k] * public_poss[k]) / \
                   (user_poss[k] * public_poss[k] + (1 - user_poss[k]) * (1 - public_poss[k]))

categories = sorted(user_poss.items(), key=lambda x: x[1], reverse=True)

book_list = []

with open(f'Categories/{categories[0][0]}.txt', 'r') as f:
    i = 0
    while i < 3:
        book_name = f.readline().strip()
        if book_name.lower() in user_read:
            continue
        book_list.append(book_name)
        i += 1

with open(f'Categories/{categories[1][0]}.txt', 'r') as f:
    i = 0
    while i < 2:
        book_name = f.readline().strip()
        if book_name.lower() in user_read:
            continue
        book_list.append(book_name)
        i += 1

with open(f'Categories/{categories[2][0]}.txt', 'r') as f:
    i = 0
    while i < 1:
        book_name = f.readline().strip()
        if book_name.lower() in user_read:
            continue
        book_list.append(book_name)
        i += 1

say("Alright " + user + " here are your recommended books", engine)
print(book_list)

book1 = cv2.imread(f"pictures/{book_list[0]}.jpeg")
book1 = cv2.resize(book1, (190, 281))
cv2.imshow("book1", book1)

book2 = cv2.imread(f"pictures/{book_list[1]}.jpeg")
book2 = cv2.resize(book2, (190, 281))
cv2.imshow("book2", book2)

book3 = cv2.imread(f"pictures/{book_list[2]}.jpeg")
book3 = cv2.resize(book3, (190, 281))
cv2.imshow("book3", book3)

book4 = cv2.imread(f"pictures/{book_list[3]}.jpeg")
book4 = cv2.resize(book4, (190, 281))
cv2.imshow("book4", book4)

book5 = cv2.imread(f"pictures/{book_list[4]}.jpeg")
book5 = cv2.resize(book5, (190, 281))
cv2.imshow("book5", book5)

book6 = cv2.imread(f"pictures/{book_list[5]}.jpeg")
book6 = cv2.resize(book6, (190, 281))
cv2.imshow("book6", book6)

cv2.waitKey(0)